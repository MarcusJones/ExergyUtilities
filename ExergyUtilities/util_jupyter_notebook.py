#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
#from Exergyconfig.config import *
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

    #myIPythonDir = os.getcwd() + "\..\IpythonNotebook\myIPythonDir"


    #os.getcwd() + "\..\IpythonNotebook\Profiles"

    arguments = [
                 #"jupyter lab", 
                 #"notebook",

                 #"--ipython-dir=\"{}\"".format(myIPythonDir),
                 #"--notebook-dir=\"{}\"".format(myIPythonDir),
                 #"--profile=myHomeProfile",
                 #"--pylab=inline"
                 #r"C:\Users\jon\.ipython\profile_default\startup\00-startup.py"
                 ]
    if start_file:
        #arguments.append("--file_to_run=\"{}\"".format(file_name))
        arguments.append("\"{}\"".format(start_file))

    if start_dir:
        #--NotebookApp.notebook_dir=<directory_name>
        arguments.append("--NotebookApp.notebook_dir=\"{}\"".format(start_dir))


    wholeCommand = ["jupyter lab"] + arguments

    wholeCommandString = " ".join(wholeCommand)

    print("Command - >\n", wholeCommandString)

    #p = subprocess.Popen(wholeCommandString, stdout=PIPE, stderr=PIPE, stdin=PIPE,shell=True).wait()
    p = subprocess.Popen(wholeCommandString,shell=True)

def help_notes():
    #Jupyter config file is located here:
    #C:\Users\jon\.jupyter
    print("NOTE! Jupyter (actually IPython) startup script directory {}: ".format('C:\\Users\\jon\\.ipython\\profile_default\\startup'))
    print("NOTE! Jupyter configuration file is (likely, as default) at {}: ".format(r"C:\Users\jon\.jupyter"))
    help_str = """
    Files will be run in lexicographical order, so you can control
    the execution order of files with a prefix, e.g.::

    00-first.py
    50-middle.py
    99-last.ipy
    """



if __name__ == "__main__":
    #C:\LOCAL_REPO\py_ExergyUtilities\ExergyUtilities\
    #this_dir = r"C:\LOCAL_REPO\Old_Python\MyUtilities\IpythonNotebook\myIPythonDir"

    #this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\kaggle_titanic"
    #this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\dsr_python_course"
    #this_dir = r"C:\DSR GIT courses\pandas-tutorial"
    
    
    #start_nb_dir = r"D:\LOCAL_REPO\ref_DataScienceRetreat\DSR Lecture notebooks"
    #start_nb_dir = r"C:\Users\jon\git\data-science-retreat-svm"
    start_nb_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\DSR Lecture notebooks"    
    #help_notes()
    
    this_file = None
    
    run_notebook(start_nb_dir,this_file)
#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
#from Exergyconfig.config import *
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
                 #r"C:\Users\jon\.ipython\profile_default\startup\00-startup.py"
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

def help_notes():
    #Jupyter config file is located here:
    #C:\Users\jon\.jupyter
    print("NOTE! Jupyter (actually IPython) startup script directory {}: ".format('C:\\Users\\jon\\.ipython\\profile_default\\startup'))
    print("NOTE! Jupyter configuration file is (likely, as default) at {}: ".format(r"C:\Users\jon\.jupyter"))
    help_str = """
    Files will be run in lexicographical order, so you can control
    the execution order of files with a prefix, e.g.::

    00-first.py
    50-middle.py
    99-last.ipy
    """



if __name__ == "__main__":
    #C:\LOCAL_REPO\py_ExergyUtilities\ExergyUtilities\
    #this_dir = r"C:\LOCAL_REPO\Old_Python\MyUtilities\IpythonNotebook\myIPythonDir"

    #this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\kaggle_titanic"
    #this_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\dsr_python_course"
    #this_dir = r"C:\DSR GIT courses\pandas-tutorial"
    start_nb_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\Week 00 lecture notebooks"
    start_nb_dir = r"C:\Users\jon\git\data-science-retreat-svm"
    start_nb_dir = r"D:\LOCAL_REPO\ref_DataScienceRetreat\DSR Lecture notebooks"

    help_notes()

    this_file = None

    run_notebook(start_nb_dir,this_file)
