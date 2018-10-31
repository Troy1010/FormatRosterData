##region Settings
import os
import logging
#---
vMasterThreshold = logging.DEBUG
vConsoleHandlerThreshold = logging.DEBUG
vFileHandlerThreshold = logging.DEBUG
bWriteLogFile = True
sLogFile = os.path.join(__file__,'..','FRDLog.log')
##endregion

class CallCounted:
    """Decorator to determine number of calls for a method"""

    def __init__(self,method):
        self.method=method
        self.iCount=0
        self.bWasCalled = False

    def __call__(self,*args,**kwargs):
        self.iCount+=1
        self.bWasCalled = True
        return self.method(*args,**kwargs)

    def WasCalled(self):
        if self.bWasCalled:
            return True
        return False

    def ClearWasCalledRecord(self):
        self.bWasCalled = False

class DefaultFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record,"sOverrideLevelName"):
            record.levelname = record.sOverrideLevelName
        return record

FRDLog = logging.getLogger(__name__)
FRDLog.warning = CallCounted(FRDLog.warning)
FRDLog.setLevel(vMasterThreshold)
FRDLog.addFilter(DefaultFilter())
vFormatter = logging.Formatter('%(levelname)-7s %(message)s')
#---ConsoleHandler
vConsoleHandler = logging.StreamHandler()
vConsoleHandler.setLevel(vConsoleHandlerThreshold)
vConsoleHandler.setFormatter(vFormatter)
FRDLog.addHandler(vConsoleHandler)
#---FileHandler
try:
    os.remove(sLogFile)
except (PermissionError,FileNotFoundError):
    pass
if bWriteLogFile:
    bLogFileIsOpen = False
    try:
        os.rename(sLogFile,sLogFile)
    except PermissionError:
        bLogFileIsOpen = True
    except FileNotFoundError:
        pass
    if not bLogFileIsOpen:
        vFileHandler = logging.FileHandler(sLogFile)
        vFileHandler.setFormatter(vFormatter)
        vFileHandler.setLevel(vFileHandlerThreshold)
        FRDLog.addHandler(vFileHandler)
