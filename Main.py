##region Setttings
sFileName = "ExampleStart.xlsx"
bPause = False
##endregion
##region Imports
import os
import FormatRosterData as FRD
import openpyxl
import TM_CommonPy as TM
import traceback
##endregion
try:
    with TM.WorkspaceContext("Output",bCDInto=True,bPreDelete=True):
        for sFileName in os.listdir("../res/Unformatted"):
            sFilePath = "../res/Unformatted/"+sFileName
            #---Open file
            vWorkbook = openpyxl.load_workbook(sFilePath)
            vSheet = vWorkbook.active
            vNewWorkbook = openpyxl.Workbook()
            vNewSheet = vNewWorkbook.active
            #---Edit
            bSuccess = True
            bSuccess &= FRD.SplitName(vSheet,vNewSheet)
            bSuccess &= FRD.SplitTown(vSheet,vNewSheet)
            bSuccess &= FRD.AppendOldSheet(vWorkbook,vNewSheet)
            #---Save
            print("SaveName:"+sFileName.split(".")[0]+"_Reformatted.xlsx")
            if not bSuccess:
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted(ERRORS).xlsx")
            else:
                vNewWorkbook.save(sFileName.split(".")[0]+"_Reformatted.xlsx")
except Exception as e:
    print("====================================================================")
    print("Traceback (most recent call last):")
    traceback.print_tb(e.__traceback__)
    print(e)
    print(e.__class__.__name__)
if bPause:
    TM.DisplayDone()
