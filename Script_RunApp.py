##region Settings
bPause = False
##endregion

import TM_CommonPy as TM
import os, sys

try:
    TM.Run("python FormatRosterData\\Main.py")
except Exception as e:
    TM.DisplayException(e)
    sys.exit(1)
if bPause:
    TM.DisplayDone()
