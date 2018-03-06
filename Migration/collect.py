#===============================================================================
#--- Add parent module
#===============================================================================

import sys
sys.path.append('/home/batman/git/py_ExergyUtilities')

import ExergyUtilities as xrg
from config.config import *


import unittest
import ExergyUtilities.util_inspect
#import ExergyUtilities.u

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
import yaml as yaml
log_config = yaml.load(open(ABSOLUTE_LOGGING_PATH, 'r'))
logging.config.dictConfig(log_config)

myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")



#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================


#===============================================================================
#--- SETUP external modules
#===============================================================================

#===============================================================================
#--- SETUP Custom modules
#===============================================================================

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================

def get_dotbashrc():
    logging.debug("{}".format(xrg.util_inspect.get_self()))
    

def run():
    print("run2")
    logging.debug("{}".format(xrg.util_inspect.get_self()))
    
    get_dotbashrc()
    xrg.util_inspect
    pass


if __name__ == "__main__":
    run()
