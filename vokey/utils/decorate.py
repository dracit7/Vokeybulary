
"""Defines some output decoration functions.
"""

def highlight(msg, color="33"):
  '''
    30: black
    31: red
    32: greed
    33: yellow
    34: blue
    35: purple
    36: cyan
    37: white
  '''
  return "\033[1;{0}m".format(color)+msg+"\033[0m"