import win32api, win32gui, win32ui
import win32con, win32process, win32com.client
import os, os.path
import const, _G, re
import cv2, time, random
import numpy as np
from PIL import Image, ImageGrab
from ctypes import windll
from datetime import timedelta
from datetime import datetime
from os import system
from collections import defaultdict
from copy import copy
import pytesseract as pyte

# To fix WTF windows window switching problem
Shell = None

# Cache screen for a period for better performance
LastFrameCount = -1
ScreenCache    = [-1, ImageGrab.grab().load()]

def hash_timestamp(_t=datetime.now()):
  return _t.second * 1000 + _t.microsecond // 1000

def flush():
  global LastFrameCount, ScreenCache
  LastFrameCount = -1
  ScreenCache[0] = -1

def wait(sec):
  time.sleep(sec)

def uwait(sec, rand=True):
  if rand:
    sec += random.random()
    if sec > 0.5:
      sec -= (random.random() / 3)
  wait(sec)

def bulk_get_kwargs(*args, **kwargs):
  result = []
  for info in args:
    name, default = info
    arg = kwargs.get(name)
    arg = default if arg is None else arg
    result.append(arg)
  return result

def ensure_dir_exists(path):
  path = path.split('/')
  path.pop()
  if len(path) == 0:
    return
  pwd = ''
  for _dir in path:
    pwd += f"{_dir}/"
    if not os.path.exists(pwd):
      os.mkdir(pwd)

def calc_similarity(str1, str2):
  len1, len2 = len(str1), len(str2)
  score = const.SimlBaseScore - abs(len2 - len1)
  for i in range(len1):
    for j in range(i,len2):
      if str1[i] == str2[j] or score <= 0:
        break
      score -= (j-i)
  return score

def save_image(img, filename, type):
  try:
    img.save(filename, type)
  except Exception as err:
    print("Image save failed", err, sep='\n')

def find_app_window():
  candidates = []

  def callback(handle, data):
    nonlocal candidates
    title = win32gui.GetWindowText(handle)
    regex = const.AppName
    if not re.search(regex, title):
      return True
    candidates.append((title, handle, calc_similarity(const.AppName, title)))
  
  win32gui.EnumWindows(callback, None)
  _G.AppHwnd = max(candidates, key=lambda x: x[-1])[1]

# ori: return original 4 pos of the window
def get_app_rect(ori=False):
  if _G.AppHwnd == 0:
    print("App not ready")
    return [0, 0, 0, 0]
  rect = win32gui.GetWindowRect(_G.AppHwnd)
  x, y, w, h = rect
  if not ori:
    w, h = w-x, h-y
    _G.AppRect = [x,y,w,h]
  return [x, y, w, h]

def get_window_context(rect, saveimg=False, filename=None, **kwargs):
  im = ImageGrab.grab(rect)
  if kwargs.get('canvas_only'):
    bbox = copy(rect)
    bbox[2] -= bbox[0] + const.ToolBarWidth
    bbox[3] -= bbox[1]
    bbox[0], bbox[1] = const.AppOffset
    im = im.crop(bbox)

  try:
    if saveimg and filename:
      im.save(filename)
  except Exception as err:
    print("Failed to save image:", err)

  return im if kwargs.get('imobj') else im.load()

def print_window(saveimg=False, filename=const.ScreenImageFile, **kwargs):
  return get_window_context(get_app_rect(True), saveimg, filename, **kwargs)

def activate_window(hwnd):
  global Shell
  Shell.SendKeys('%')
  pid = win32process.GetWindowThreadProcessId(hwnd)[1]
  windll.user32.AllowSetForegroundWindow(pid)
  win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
  win32gui.BringWindowToTop(hwnd)
  win32gui.SetActiveWindow(hwnd)
  windll.user32.SwitchToThisWindow(hwnd, 1)
  win32gui.SetForegroundWindow(hwnd)

# app_offset:
#  The cursor position in the app instead of the monitor
def get_cursor_pos(app_offset=True):
  mx, my = win32api.GetCursorPos()
  if app_offset:
    offset = const.AppOffset
    mx = mx - _G.AppRect[0] - offset[0]
    my = my - _G.AppRect[1] - offset[1]
  return [mx, my]

def set_cursor_pos(x, y, app_offset):
  if app_offset:
    offset = const.AppOffset
    x += _G.AppRect[0] + offset[0]
    y += _G.AppRect[1] + offset[1]
  win32api.SetCursorPos((x,y))

def get_app_pixel(x=None, y=None):
  global LastFrameCount, ScreenCache
  
  if LastFrameCount != _G.FrameCount:
    LastFrameCount = _G.FrameCount
    stamp = hash_timestamp()
    if abs(ScreenCache[0] - stamp) > const.ScreenCacheTimeout:
      ScreenCache[0] = stamp
      ScreenCache[1] = print_window()
      
  if x and y:
    x += const.AppOffset[0]
    y += const.AppOffset[1]
    return ScreenCache[1][x, y]
  return ScreenCache[1]

def read_app_text(x, y, x2, y2, **kwargs):
  rect = get_app_rect(True)
  offset = const.AppOffset
  x, y = x + offset[0], y + offset[1]
  x2, y2 = x2 + offset[0], y2 + offset[1]
  rect[2], rect[3] = rect[0] + x2, rect[1] + y2
  rect[0], rect[1] = rect[0] + x,  rect[1] + y
  im = ImageGrab.grab(rect)
  filename = const.OCR_Filename
  save_image(im, filename, "PNG")
  uwait(0.3) # wait os to update index
  return img_to_str(filename, **kwargs)

def img_to_str(filename, **kwargs):
  dtype, lan = bulk_get_kwargs(
    ('dtype', None), ('lan', 'eng'),
    **kwargs
  )
  if _G.Flags['log-level'] > 0:
    print("----------\nOCR Processing")
  _config = const.OCR_ARGS
  rescues = 2
  result = None
  last_err = None
  for _ in range(rescues+1):
    try:
      result = pyte.image_to_string(filename, config=_config, lang=lan)
      break
    except Exception as err:
      last_err = err
      if "unknown command line argument '-psm'" in str(err):
        _config = _config.replace('-psm', '--psm')
        continue
      if "TESSDATA_PREFIX" in str(err):
        os.environ['TESSDATA_PREFIX'] += '/tessdata'
        continue
      raise(err)
  if not result and last_err:
    raise(last_err)
  if dtype == 'digit':
    result = correct_digit_result(result)
  elif dtype == 'time':
    result = correct_time_result(result)
  elif dtype == 'alpha':
    result = correct_alphabet_result(result)
  
  if _G.Flags['log-level'] > 0:
    print("OCR Result:\n{}\n".format(result))
  return result

def sec2readable(secs):
  return str(timedelta(seconds=secs))

def correct_digit_result(result):
  if _G.Flags['log-level'] > 0:
    print("Before digit tr:", result)
  result = result.translate(str.maketrans(const.OCR_DigitTrans))
  return ''.join(ch for ch in result if ch.isdigit())

def correct_time_result(result):
  if _G.Flags['log-level'] > 0:
    print("Before time tr:", result)
  result = result.translate(str.maketrans(const.OCR_TimeTrans))
  return ''.join(ch for ch in result if ch.isdigit() or ch == ':')

def correct_alphabet_result(result):
  result = result.translate(str.maketrans(const.OCR_AlphaTrans))
  return ''.join(ch for ch in result if ch.isalpha())

def init():
  global Shell
  Shell = win32com.client.Dispatch("WScript.Shell")
  ensure_dir_exists(const.ScreenImageFile)
  find_app_window()
  get_app_rect()