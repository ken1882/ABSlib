AppHwnd = 0

BaseUpdateFactor = 120
UpdateDuration   = (1 / BaseUpdateFactor)
ScriptUpdateTime = BaseUpdateFactor
CurScriptTick    = BaseUpdateFactor

def change_update_speed(n):
  global BaseUpdateFactor, UpdateDuration
  global ScriptUpdateTime, CurScriptTick
  BaseUpdateFactor = n
  UpdateDuration   = (1 / BaseUpdateFactor)
  ScriptUpdateTime = BaseUpdateFactor
  CurScriptTick    = BaseUpdateFactor

Flags = {
  'running': True,
  'paused': False
}