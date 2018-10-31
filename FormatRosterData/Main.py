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
from FormatRosterData._Logger import vFormatter #awkward
import logging
##endregion

def Main():
    with TM.WorkspaceContext("Output",bCDInto=True,bPreDelete=True):
        #-Add Report_Full.txt handler to FRDLog
        vFileHandler = logging.FileHandler("__Report_Full.txt")
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(1)
        FRDLog.addHandler(vFileHandler)
        #-
        cUnmatchedFileNames = []
        cFormattingErrorFileNames = []
        cWorkbooksToReformat = [] #Expects value to be tuple(vOldWorkbook,sFileName)
        #---Output cNameToURL_Men.txt, cNameToURL_Women.txt
        FRDLog.info("---Getting NameToURL lists---")
        cNameToURL_Men = FRD.GetDict_NameToURL_Men()
        FRD.WriteDictToTxtFile(cNameToURL_Men,'__cNameToURL_Men.txt')
        FRDLog.info("__cNameToURL_Men.txt complete")
        cNameToURL_Women = FRD.GetDict_NameToURL_Women()
        FRD.WriteDictToTxtFile(cNameToURL_Women,'__cNameToURL_Women.txt')
        FRDLog.info("__cNameToURL_Women.txt complete")
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
                            cUnmatchedFileNames.append(sLine)
                            FRDLog.info(sFileName+" - Could not match:"+sLine)
            else:
                cUnmatchedFileNames.append(sFileName)
                FRDLog.warning("Could not get workbook from file:"+sFileName)
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
                sFileName = "_ERRORS_"+sFileName.split(".")[0]+"_Reformatted.xlsx"
                cFormattingErrorFileNames.append(sFileName)
            else:
                sFileName = sFileName.split(".")[0]+"_Reformatted.xlsx"
            FRDLog.info("New_FileName:"+sFileName)
            vNewWorkbook.save(sFileName)
        #---Report
        FRDLog.info("---Report---")
        #-Add Report.txt handler to FRDLog
        vFileHandler = logging.FileHandler("__Report.txt")
        vFileHandler.setFormatter(logging.Formatter('%(message)s'))
        vFileHandler.setLevel(1)
        FRDLog.addHandler(vFileHandler)
        #-
        if cFormattingErrorFileNames:
            FRDLog.info("\t"+str(len(cFormattingErrorFileNames)) + " ERROR FILES")
            for sFileName in cFormattingErrorFileNames:
                FRDLog.info(sFileName)
        else:
            FRDLog.info("There were no errors.")
        if cUnmatchedFileNames:
            FRDLog.info("\t"+str(len(cUnmatchedFileNames)) + " UNMATCHED")
            for sFileName in cUnmatchedFileNames:
                FRDLog.info(sFileName)
        else:
            FRDLog.info("There were no unmatched files.")
        #-Remove temporary handlers from FRDLog
        FRDLog.handlers = [h for h in FRDLog.handlers if hasattr(h,"baseFilename") and not "report" in os.path.basename(h.baseFilename).lower()]


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
