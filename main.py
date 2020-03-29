import sys
sys.path.append('./lib')
import _G, const, util, Input

def start():
  util.init()
  
  if _G.AppHwnd == 0:
    print("App not found, aborting")
    return exit()

  util.activate_window(_G.AppHwnd)
  while _G.Flags['running']:
    main_loop()

def main_loop():
  util.uwait(_G.UpdateDuration, False)
  
  update_basic()
  _G.CurScriptTick += 1
  
  if _G.CurScriptTick >= _G.ScriptUpdateTime:
    _G.CurScriptTick = 0
    if not _G.Flags['paused']:
      update_script()
      Input.clear_cache()

def update_basic():
  update_input()

def update_input():
  Input.update()
  # pause program
  if Input.is_trigger(Input.keymap.kF8, True):
    _G.Flags['paused'] ^= True
    print(f"Paused: {_G.Flags['paused']}")
  
  # terminate program
  elif Input.is_trigger(Input.keymap.kF9, True):
    _G.Flags['running'] = False

def update_script():
  util.get_app_rect()


start()