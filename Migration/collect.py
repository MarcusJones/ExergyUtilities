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

import shutil


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

#--- Utilities

class AFile():
    def __init__(self,src_root,src_path,src_name):
        self.src_root   = src_root
        self.src_path   = src_path
        self.src_name   = src_name
        logging.debug("Created source file {}".format(self.src_path_full))
    
    def add_target_root(self,tgt_root):
        self.tgt_root   = tgt_root
        self.tgt_path   = self.src_path
        self.tgt_name   = self.src_name      
    

    @property
    def src_path_full(self):
        return os.path.join(self.src_root, self.src_path, self.src_name)

    @property
    def tgt_path_full(self):
        return os.path.join(self.tgt_root, self.src_path, self.src_name)
        
    @property
    def src_exists(self):
        return os.path.exists(self.src_path_full)

    @property
    def tgt_exists(self):
        return os.path.exists(self.tgt_path_full)

    def copy_src_tgt(self):
        os.makedirs(os.path.dirname(self.tgt_path_full), exist_ok=True)
        shutil.copy2(self.src_path_full,self.tgt_path_full)    
        logging.debug("Copied {} -> {}".format(self.src_name, self.tgt_path))








def run():
    print("run2")
    
    src_root = os.path.expanduser("~")
    tgt_root = r"/home/batman/git/py_ExergyUtilities/Migration/home/usr"
    
    files = list()
    
    #--- .bashrc 
    print(".bashrc")    
    files.append(AFile(src_root,'','.bashrc'))

    #--- mj.sh
    print("mj.sh")
    files.append(AFile(src_root,'','mj.sh'))
    
    #--- Jupyter Lab startup script (ipython startup)
    print("Jupyter Lab startup script (ipython startup)")
    files.append(AFile(src_root,'.ipython/profile_default/startup','00 MJ.py'))
    
    #--- Atom packages
    print("Atom packages are starred in the server")

    #--- Eclipse theme
    print("Atom packages are starred in the server")
    
    #--- Eclipse run configurations for projects (python env)

    
    for f in files:
        print('SRC', f.src_exists,f.src_path_full)
        f.add_target_root(tgt_root)
        print('TGT', f.tgt_exists, f.tgt_path_full)
        f.copy_src_tgt()
        #print(f.)
    
    #print(bashrc)
    
    
    logging.debug("{}".format(xrg.util_inspect.get_self()))
    
    
    #this_file = get_dotbashrc(current_home_dir)
    
    

if __name__ == "__main__":
    run()
