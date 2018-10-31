##region Setttings
sInputFolderPath = "../res/Input"
bPause = True
bSkipScrapping = False
##endregion
##region Imports
import os
import FormatRosterData as FRD
import openpyxl
import TM_CommonPy as TM
import traceback
from FormatRosterData._Logger import FRDLog
##endregion

def Main():
    with TM.WorkspaceContext("Output",bCDInto=True,bPreDelete=True):
        iTotalErrorFileCount = 0
        cWorkbooksToReformat = [] #Expects value to be tuple(vOldWorkbook,sFileName)
        #---Output cNameToURL_Men.txt, cNameToURL_Women.txt
        FRDLog.info("---Getting NameToURL lists---")
        cNameToURL_Men = FRD.GetDict_NameToURL_Men()
        with open('cNameToURL_Men.txt','w') as vFile:
            for vKey, vValue in cNameToURL_Men.items():
                vFile.write(vKey + " : " + vValue + "\n")
        FRDLog.info("cNameToURL_Men.txt complete")
        cNameToURL_Women = FRD.GetDict_NameToURL_Women()
        with open('cNameToURL_Women.txt','w') as vFile:
            for vKey, vValue in cNameToURL_Women.items():
                vFile.write(vKey + " : " + vValue + "\n")
        FRDLog.info("cNameToURL_Women.txt complete")
        #---Get OldWorkbooks
        FRDLog.info("---Collecting unformatted sheets---")
        for sFileName in os.listdir(sInputFolderPath):
            if (not sFileName.split(".")[-1] in ["xlsx","txt"]) or "~$" in sFileName or "template" in sFileName.lower():
                FRDLog.info("IGNORED:"+sFileName)
                continue
            elif sFileName.split(".")[-1] == "xlsx":
                vOldWorkbook = openpyxl.load_workbook(os.path.join(sInputFolderPath,sFileName))
                cWorkbooksToReformat.append((vOldWorkbook,sFileName))
            elif sFileName.split(".")[-1] == "txt" and not bSkipScrapping:
                #-Determine cNameToURL
                if "women" in sFileName.lower():
                    bWomen = True
                    cNameToURL = cNameToURL_Women
                else:
                    bWomen = False
                    cNameToURL = cNameToURL_Men
                #-
                with open(os.path.join(sInputFolderPath,sFileName),'r') as vTextFile:
                    for sLine in vTextFile.readlines():
                        sLine = sLine.rstrip('\n') #probs a better way to do this.
                        if not sLine:
                            continue
                        for vKey in cNameToURL.keys():
                            if sLine.lower() in vKey.lower():
                                FRDLog.info(sFileName+" -  MATCHED:"+sLine+"("+vKey+")")
                                if bWomen:
                                    vOldWorkbook = FRD.GetWorkbook_Women(cNameToURL[vKey])
                                    sScrapedFileName = "Scraped_"+FRD.GetTitle(cNameToURL[vKey])+"_Women" #important so that program knows not to look for weight.
                                else:
                                    vOldWorkbook = FRD.GetWorkbook_Men(cNameToURL[vKey])
                                    sScrapedFileName = "Scraped_"+FRD.GetTitle(cNameToURL[vKey])+"_Men"
                                cWorkbooksToReformat.append((vOldWorkbook,sScrapedFileName))
                                break
                        else:
                            FRDLog.info(sFileName+" - Could not match:"+sLine)
            else:
                iTotalErrorFileCount += 1
                FRDLog.warning("Could not get workbook from sFileName:"+sFileName)
                continue
        #---Create NewWorkbooks
        FRDLog.info("---Creating formatted sheets---")
        FRDLog.warning.ClearWasCalledRecord()
        for vOldWorkbook, sFileName in cWorkbooksToReformat:
            FRDLog.info("OldFileName:"+sFileName)
            #---Edit
            vOldSheet = vOldWorkbook.active
            vNewWorkbook = openpyxl.Workbook()
            vNewSheet = vNewWorkbook.active
            FRD.FormatName(vOldSheet,vNewSheet)
            FRD.FormatHometown(vOldSheet,vNewSheet)
            FRD.FormatHeight(vOldSheet,vNewSheet)
            if not "women" in sFileName.lower():
                FRD.FormatWeight(vOldSheet,vNewSheet)
            FRD.FormatSchoolyear(vOldSheet,vNewSheet)
            FRD.FormatPosition(vOldSheet,vNewSheet)
            FRD.AppendOldSheet(vOldSheet,vNewSheet)
            #---Save
            if FRDLog.warning.WasCalled():
                FRDLog.warning.ClearWasCalledRecord()
                iTotalErrorFileCount += 1
                sFileName = "aa(ERRORS)_"+sFileName.split(".")[0]+"_Reformatted.xlsx"
            else:
                sFileName = sFileName.split(".")[0]+"_Reformatted.xlsx"
            FRDLog.info("New_FileName:"+sFileName)
            vNewWorkbook.save(sFileName)


    if iTotalErrorFileCount:
        FRDLog.info("TOTAL ERROR FILES`iTotalErrorFileCount:"+str(iTotalErrorFileCount))
    else:
        FRDLog.info("Success`iTotalErrorFileCount:"+str(iTotalErrorFileCount))

try:
    Main()
except PermissionError:
    FRDLog.error("\n\tI'd recommend to just try again.\n\tOtherwise, close all extra programs and then retry.",extra={'sOverrideLevelName': "PERMISSION_ERROR"})
    TM.DisplayDone()
except Exception as e:
    TM.DisplayException(e)
else:
    if bPause:
        TM.DisplayDone()
