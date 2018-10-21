##region Settings
bPause = False
##endregion

import TM_CommonPy as TM
import os, sys

try:
    TM.Delete("ExampleStart_Reformatted.xlsx")
    TM.Delete("ExampleStart_Reformatted(ERRORS).xlsx")
    TM.Run("python FormatRosterData\\Main.py")
except Exception as e:
    TM.DisplayException(e)
    sys.exit(1)
if bPause:
    TM.DisplayDone()
