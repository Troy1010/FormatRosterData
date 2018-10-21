##region Settings
bSkip=False
bSkipSome=False
bPostDelete=False
##endregion
import unittest
from nose.tools import *
import os, sys
import TM_CommonPy as TM
import FormatRosterData as FRD
from FormatRosterData._Logger import FRDLog

@unittest.skipIf(bSkip,"Skip Setting")
class Test_FormatRosterData(unittest.TestCase):
    sTestWorkspace = "TestWorkspace/"

    @classmethod
    def setUpClass(self):
        os.chdir(os.path.join('FormatRosterData','tests'))
        TM.Delete(self.sTestWorkspace)

    @classmethod
    def tearDownClass(self):
        global bPostDelete
        if bPostDelete:
            TM.Delete(self.sTestWorkspace)
        os.chdir(os.path.join('..','..'))

    # ------Tests

    @unittest.skipIf(bSkipSome,"SkipSome Setting")
    def test_DummyTest(self):
        with TM.CopyContext("res/Examples_Backup",self.sTestWorkspace+TM.FnName(),bPostDelete=False):
            print(os.getcwd())
            vSheet = FRD.LoadSheet("ExampleStart.xlsx")
            FRDLog.debug(vSheet['A1'].value)
            FRDLog.debug(vSheet['A2'].value)
            FRD.Hello()
