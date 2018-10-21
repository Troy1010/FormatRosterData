import os
import openpyxl

def GetPos(vCell,iColAdjustment=0):
    return openpyxl.utils.get_column_letter(openpyxl.utils.column_index_from_string(vCell.column)+iColAdjustment)+str(vCell.row)

def SplitName(vOldSheet,vNewSheet):
    bSuccess = True
    i=1
    for vCell in vOldSheet['A']:
        cSplitString = vCell.value.split(" ")
        if len(cSplitString) >2:
            bSuccess = False
            print("ERROR`Name's cSplitString > 2. There is a name with too many words.")
        vNewSheet['A'+str(i)] = cSplitString[0]
        vNewSheet['B'+str(i)] = cSplitString[1]
        i=i+1
    return bSuccess

def AppendOldSheet(vOldWorkspace,vNewSheet):
    iMaxCol = len(vNewSheet['1'])
    for cColumn in vOldWorkspace.active.iter_cols():
        for vCell in cColumn:
            vNewSheet[GetPos(vCell,iColAdjustment=iMaxCol+1)] = vCell.value
