import win32api, win32con
import random
import _G, const
from util import wait, uwait, bulk_get_kwargs

def key_down(*args):
  for kid in args:
    win32api.keybd_event(kid, 0, 0, 0)

def key_up(*args):
  for kid in args:
    win32api.keybd_event(kid, 0, win32con.KEYEVENTF_KEYUP, 0)

def trigger_key(*args):
  for kid in args:
    key_down(kid)
  uwait(0.03)
  for kid in args:
    key_up(kid)

def mouse_down(x, y, app_offset):
  if app_offset:
    offset = const.getAppOffset()
    x += _G.AppRect[0] + offset[0]
    y += _G.AppRect[1] + offset[1]
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)

def mouse_up(x, y, app_offset):
  if app_offset:
    offset = const.getAppOffset()
    x += _G.AppRect[0] + offset[0]
    y += _G.AppRect[1] + offset[1]
  win32api.SetCursorPos((x,y))
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def set_cursor_pos(x, y, app_offset):
  if app_offset:
    offset = const.getAppOffset()
    x += _G.AppRect[0] + offset[0]
    y += _G.AppRect[1] + offset[1]
  win32api.SetCursorPos((x,y))

def click(x, y, app_offset=True):
  set_cursor_pos(x, y, app_offset)
  mouse_down(x, y, app_offset)
  mouse_up(x, y, app_offset)

def scroll_up(x, y, delta = 100, app_offset=True, haste=False):
  mouse_down(x, y, app_offset)
  ty = y + delta
  wait(0.01 if haste else 0.5)
  while y <= ty:
    y += (random.randint(*const.MouseScrollDelta) + haste * 2)
    set_cursor_pos(x, min([y,ty]), app_offset)
    wait(0.01 if haste else const.MouseScrollTime)
  mouse_up(x, y, app_offset)

def scroll_down(x, y, delta = 100, app_offset=True, haste=False):
  mouse_down(x, y, app_offset)
  ty = y - delta
  wait(0.01 if haste else 0.5)
  while y >= ty:
    y -= (random.randint(*const.MouseScrollDelta) + haste * 2)
    set_cursor_pos(x, max([y,ty]), app_offset)
    wait(0.01 if haste else const.MouseScrollTime)
  mouse_up(x, y, app_offset)

def scroll_left(x, y, delta = 100, app_offset=True, haste=False):
  mouse_down(x, y, app_offset)
  tx = x + delta
  wait(0.01 if haste else 0.5)
  while x <= tx:
    x += (random.randint(*const.MouseScrollDelta) + haste * 2)
    set_cursor_pos(min([x,tx]), y, app_offset)
    wait(0.01 if haste else const.MouseScrollTime)
  mouse_up(x, y, app_offset)

def scroll_right(x, y, delta = 100, app_offset=True, haste=False):
  mouse_down(x, y, app_offset)
  tx = x - delta
  wait(0.01 if haste else 0.5)
  while x >= tx:
    x -= (random.randint(*const.MouseScrollDelta) + haste * 2)
    set_cursor_pos(max([x,tx]), y, app_offset)
    wait(0.01 if haste else const.MouseScrollTime)
  mouse_up(x, y, app_offset)

def scroll_to(x, y, x2, y2, **kwargs):
  app_offset,haste,hold = bulk_get_kwargs(
    ('app_offset', True), ('haste', False), ('hold', True),
    **kwargs
    )
  
  mouse_down(x, y, app_offset)
  wait(0.01 if haste else const.MouseScrollTime)
  tdx, tdy = abs(x2 - x), abs(y2 - y)
  try:
    pcx, pcy = tdx // tdy, tdy // tdx
    pcx, pcy = min([max([pcx, 0.4]), 2]), min([max([pcy, 0.4]), 2])
  except Exception:
    pcx, pcy = 1, 1

  while x != x2 or y != y2:
    dx = int((random.randint(*const.MouseScrollDelta) + haste * 2) * pcx)
    dy = int((random.randint(*const.MouseScrollDelta) + haste * 2) * pcy)
    x = min([x2, x+dx]) if x2 > x else max([x2, x-dx])
    y = min([y2, y+dy]) if y2 > y else max([y2, y-dy])
    set_cursor_pos(x, y, app_offset)
    wait(0.01 if haste else const.MouseScrollTime)
  if hold:
    uwait(1)
  mouse_up(x, y, app_offset)

def random_click(x, y, rrange=const.DefaultRandRange):
  if rrange is None:
    rrange = const.DefaultRandRange
  click(x + random.randint(-rrange,rrange), y + random.randint(-rrange,rrange))

def random_scroll_to(x, y, x2, y2, **kwargs):
  rrange = kwargs.get('rrange')
  rrange = const.DefaultRandRange if rrange is None else rrange
  x += random.randint(-rrange, rrange)
  y += random.randint(-rrange, rrange)
  x2 += random.randint(-rrange, rrange)
  y2 += random.randint(-rrange, rrange)
  scroll_to(x, y, x2, y2, **kwargs)