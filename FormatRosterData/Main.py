##region Setttings
sFileName = "ExampleStart.xlsx"
##endregion
##region Imports
import os
import pandas as pd
import FormatRosterData as FRD
##endregion

vSheet = FRD.LoadSheet(sFileName)
print(vSheet['A1'].value)
print(vSheet['A2'].value)
