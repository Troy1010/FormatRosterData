import os
import openpyxl

def Hello():
    print("Hi")

def LoadSheet(sWorkbookFilePath):
    vWorkbook = openpyxl.load_workbook(sWorkbookFilePath)
    return vWorkbook.active
