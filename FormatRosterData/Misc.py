import os
import openpyxl
import TM_CommonPy as TM

def GetPos(vCell,iColAdjustment=0):
    return openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(vCell.column)+iColAdjustment)+str(vCell.row)

def SplitName(vOldSheet,vNewSheet):
    iMaxCol = len(vNewSheet['1'])
    bSuccess = True
    for vCell in vOldSheet['B']:
        cSplitString = vCell.value.split(" ",1)
        vNewSheet[openpyxl.utils.get_column_letter(iMaxCol)+str(vCell.row)] = cSplitString[0]
        vNewSheet[openpyxl.utils.get_column_letter(iMaxCol+1)+str(vCell.row)] = cSplitString[1]
    return bSuccess

def SplitTown(vOldSheet,vNewSheet):
    iMaxCol = len(vNewSheet['1'])
    bSuccess = True
    #---Determine Town Column
    bStart=False
    for vCell in vOldSheet['1']:
        if vCell.column == "F":
            bStart=True
        if bStart:
            if TM.MsgBox("Is this a city?\n\t"+str(vCell.value),iStyle=4) == 6: #(yes)
                sColumn = vCell.column
                break
    else:
        print("Unable to find city column")
        return False
    #---
    for vCell in vOldSheet[sColumn]:
        cSplitString = vCell.value.split(" ")
        cSplitString[0] = cSplitString[0][:-1]
        vNewSheet[openpyxl.utils.get_column_letter(iMaxCol)+str(vCell.row)] = cSplitString[0]
        vNewSheet[openpyxl.utils.get_column_letter(iMaxCol+1)+str(vCell.row)] = cSplitString[1]
    return bSuccess

def AppendOldSheet(vOldWorkspace,vNewSheet):
    iMaxCol = len(vNewSheet['1'])
    bSuccess = True
    for cColumn in vOldWorkspace.active.iter_cols():
        for vCell in cColumn:
            vNewSheet[GetPos(vCell,iColAdjustment=iMaxCol+1)] = vCell.value
    return bSuccess
