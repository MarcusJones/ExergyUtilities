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
#--- SETUP Standard modules
#===============================================================================
import subprocess
import sys
import os
#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================

#--- Main


def run_notebook(start_dir = None, start_file=None):
    #profilesDir = os.getcwd() + "\..\IpythonNotebook\Profiles"
    
    myIPythonDir = os.getcwd() + "\..\IpythonNotebook\myIPythonDir"
    
    
    #os.getcwd() + "\..\IpythonNotebook\Profiles"
    
    arguments = [
                 "notebook", 

                 #"--ipython-dir=\"{}\"".format(myIPythonDir),
                 #"--notebook-dir=\"{}\"".format(myIPythonDir),
                 #"--profile=myHomeProfile",
                 #"--pylab=inline"

                 ]
    if start_file:
        #arguments.append("--file_to_run=\"{}\"".format(file_name))
        arguments.append("\"{}\"".format(start_file))
        
    if start_dir:
        arguments.append("--notebook-dir=\"{}\"".format(start_dir))
        

    wholeCommand = ["jupyter"] + arguments
    
    wholeCommandString = " ".join(wholeCommand)
    
    print("Command - >\n", wholeCommandString)
    
    #p = subprocess.Popen(wholeCommandString, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True).wait()
    p = subprocess.Popen(wholeCommandString,shell=True)

    
    
if __name__ == "__main__":
    #print("ss")
    #C:\LOCAL_REPO\py_ExergyUtilities\ExergyUtilities\
    #this_dir = r"C:\LOCAL_REPO\Old_Python\MyUtilities\IpythonNotebook\myIPythonDir"
    
    #this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\kaggle_titanic"
    this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\dsr_python_course"
    this_dir = r"C:\DSR GIT courses\pandas-tutorial"
    
    #Jupyter config file is located here:
    #"C:\Users\jon\.jupyter"
    
    #this_file = r"LP 01 - Lesson.ipynb"
    #this_file =r"Lecture-1-Introduction-to-Python-Programming.ipynb"
    this_file = None
    
    run_notebook(this_dir,this_file)
