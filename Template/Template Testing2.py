# TEST MODULE
#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")


#===============================================================================
#--- SETUP Add parent module
#===============================================================================
#from os import sys, path
import os
# Add parent to path
if __name__ == '__main__' and __package__ is None:
    this_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
from ExergyUtilities.utility_inspect import get_self

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.utility_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- Unit testing
#===============================================================================
print("Test")
class BasicTest(unittest.TestCase):
    def setUp(self):
        #print "**** TEST {} ****".format(get_self())
        myLogger.setLevel("CRITICAL")
        print("Setup")
         
        curr_path = os.path.dirname(os.path.realpath(__file__))
        curr_path = os.path.abspath(curr_path + "\..\..\ExcelTemplates\Table test.xlsx")
         
        myLogger.setLevel("DEBUG")
         
         
    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
         

#--- This line makes is more clear how to run in Eclipse
#--- Check to make sure this runs first (Run as -> python)
if __name__ == '__main__': 
    unittest.main()

