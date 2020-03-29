# Window Title
AppName = "BlueStacks"

# Base similarity score
SimlBaseScore = 100

# Offset to the android render from window position
AppOffset    = (3, 42)
ToolBarWidth = 66

# Default path to save the window image
ScreenImageFile = "tmp/window.png"

# Time delta when scrolling the screen
MouseScrollTime  = 0.03

# Distance delta when scrolling screen
MouseScrollDelta = [3,8]

# Default range for randomized coordinate actions
DefaultRandRange = 6

# Color value toleration
ColorTolerateRange = 10

ScreenCacheTimeout = 1000 # ms

OCR_Filename = 'tmp/apptext.png'

OCR_ARGS = '-psm 12 -psm 13'
OCR_DigitTrans = {
  'O': '0',
  'o': '0',
}

OCR_TimeTrans  = {
  'O': '0',
  'o': '0',
}

OCR_AlphaTrans = {
  '|': 'l',
  '§': 's',
  '5': 's',
  '0': '0',
}