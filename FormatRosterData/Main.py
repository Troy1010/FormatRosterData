##region Setttings
sFileName = "ExampleStart.xlsx"
##endregion
##region Imports
import os
import pandas as pd
import FormatRosterData as FRD
import openpyxl
##endregion
vWorkbook = openpyxl.load_workbook(sFileName)
vSheet = vWorkbook.active
vNewWorkbook = openpyxl.Workbook()
vNewSheet = vNewWorkbook.active
#---Edit
bSuccess = True
bSuccess = FRD.SplitName(vSheet,vNewSheet)
FRD.AppendOldSheet(vWorkbook,vNewSheet)
#---Save
if not bSuccess:
    vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
else:
    vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted.xlsx")
