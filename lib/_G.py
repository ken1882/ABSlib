AppHwnd = 0

# Window Rect
AppRect = [0, 0, 0, 0]

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
  'verbose': True,
  'log-level': 0,
  'running': True,
  'paused': False
}

Flags['log-level'] += 1 if Flags['verbose'] else 0
FrameCount = 0