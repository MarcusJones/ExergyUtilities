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

my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")



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
import os


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

#---Utilities

class AFile():
    def __init__(self,fname):
        self.fname = fname
        self.path_source = None
        self.path_full = None
    def set_source_path(self,path_source):
        self.path_source = path_source
        self.path_full = os.path.join(self.path_source,self.fname)
        assert os.path.exists(self.path_full), "{} does not exist".format(self.path_full)
    
    def __repr__(self):
        rstring = "Path object at "
        if self.path_full:
            rstring += self.path_full
        if os.path.exists(self.path_full):
            rstring += ' Exists'
        return(rstring)
    
#--- Atom packages
print("Atom packages are starred in the server")

#--- Eclipse theme

#--- Eclipse run configurations for projects (python env)

#--- .bashrc 

#--- mj.sh

#--- Jupyter Lab startup script (ipython startup)



# def get_dotbashrc(home_dir):
#     logging.debug("{}".format(xrg.util_inspect.get_self()))
#     fname = ".bashrc"
#     fullpath = 
#     
#     
#     return fullpath
    

def run():
    print("run2")
    
    home_dir = os.path.expanduser("~")
    
    
    bashrc = AFile('.bashrc')
    bashrc.set_source_path(home_dir)
    
    print(bashrc)
    
    
    logging.debug("{}".format(xrg.util_inspect.get_self()))
    
    
    #this_file = get_dotbashrc(current_home_dir)
    
    

if __name__ == "__main__":
    run()
