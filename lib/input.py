import win32api, win32con
import random
import _G, const
from util import wait, uwait, bulk_get_kwargs

# immediate keystate at current frame
keystate = [0 for _ in range(0xff)]

# keystate for scipt calls
keystate_cache = [0 for _ in range(0xff)]

class keymap:
  kMOUSE1 = 1
  kMOUSE2 = 2
  kMOUSE3 = 3
  k0 = 48
  k1 = 49
  k2 = 50
  k3 = 51
  k4 = 52
  k5 = 53
  k6 = 54
  k7 = 55
  k8 = 56
  k9 = 57
  kA = 65
  kB = 66
  kC = 67
  kD = 68
  kE = 69
  kF = 70
  kG = 71
  kH = 72
  kI = 73
  kJ = 74
  kK = 75
  kL = 76
  kM = 77
  kN = 78
  kO = 79
  kP = 80
  kQ = 81
  kR = 82
  kS = 83
  kT = 84
  kU = 85
  kV = 86
  kW = 87
  kX = 88
  kY = 89
  kZ = 90
  kENTER = 13
  kRETURN = 13
  kBACKSPACE = 8
  kSPACE = 32
  kESCAPE = 27
  kESC = 27
  kSHIFT = 16
  kTAB = 9
  kALT = 18
  kCTRL = 17
  kCONTROL = 17
  kDELETE = 46
  kDEL = 46
  kINSERT = 45
  kINS = 45
  kPAGEUP = 33
  kPUP = 33
  kPAGEDOWN = 34
  kPDOWN = 34
  kHOME = 36
  kEND = 35
  kLALT = 164
  kLCTRL = 162
  kRALT = 165
  kRCTRL = 163
  kLSHIFT = 160
  kRSHIFT = 161
  kLEFT = 37
  kRIGHT = 39
  kUP = 38
  kDOWN = 40
  kCOLON = 186
  kAPOSTROPHE = 222
  kQUOTE = 222
  kCOMMA = 188
  kPERIOD = 190
  kSLASH = 191
  kBACKSLASH = 220
  kLEFTBRACE = 219
  kRIGHTBRACE = 221
  kMINUS = 189
  kUNDERSCORE = 189
  kPLUS = 187
  kEQUAL = 187
  kEQUALS = 187
  kTILDE = 192
  kF1 = 112
  kF2 = 113
  kF3 = 114
  kF4 = 115
  kF5 = 116
  kF6 = 117
  kF7 = 118
  kF8 = 119
  kF9 = 120
  kF10 = 121
  kF11 = 122
  kF12 = 123
  kArrows = 224

def update():
  global keystate, keystate_cache
  for i in range(0xff):
    if win32api.GetAsyncKeyState(i):
      keystate[i] += 1
      keystate_cache[i] += 1
    else:
      keystate[i] = 0

def clear_cache():
  for i in range(0xff):
    keystate_cache[i] = 0

def is_trigger(i, immediate):
  if not immediate:
    return keystate_cache[i] > 0 and keystate_cache[i] <= _G.ScriptUpdateTime
  return keystate[i] == 1

def is_press(i, immediate):
  if not immediate:
    return keystate_cache[i] > 0
  return keystate[i] > 0

def is_repeat(i, immediate):
  if not immediate:
    return keystate_cache[i] // _G.ScriptUpdateTime
  return keystate[i]

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