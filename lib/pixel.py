import _G, const
import util

def is_color_ok(cur, target):
  for c1,c2 in zip(cur,target):
    if _G.Flags['log-level'] > 1:
      print('-'*10)
      print(c1, c2)
    if abs(c1 - c2) > const.ColorTolerateRange:
      return False
  return True

# indr:
#  get individual result of each pixel instead of
#  single result whether all-matched
def is_pixels_match(pix, col, indr=False):
  ret = []
  for i, j in zip(pix, col):
    tx, ty = i
    ok = is_color_ok(util.get_app_pixel(tx, ty), j)
    if not ok and not indr:
      return False
    else:
      ret.append(ok)
  
  return ret if indr else True