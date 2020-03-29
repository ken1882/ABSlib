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

Shell = None

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

def ensure_dir_exist(path):
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

def get_window_pixels(rect, saveimg=False, filename=None, **kwargs):
  im = ImageGrab.grab(rect)
  if kwargs['canvas_only']:
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
  pixels = im.load()
  return pixels

def print_window(saveimg=False, filename=const.ScreenImageFile, **kwargs):
  return get_window_pixels(get_app_rect(True), saveimg, filename, **kwargs)

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

def init():
  global Shell
  Shell = win32com.client.Dispatch("WScript.Shell")
  ensure_dir_exist(const.ScreenImageFile)
  find_app_window()
  get_app_rect()