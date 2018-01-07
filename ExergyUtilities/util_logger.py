#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B. 
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
    

from config import *

import logging.config
import unittest

LOGGING_CONFIG_1 = '%(funcName)-20s %(levelno)-3s: %(message)s'
LOGGING_CONFIG_2 = '%(module)-20s %(funcName)-20s %(levelno)-3s: %(message)s'

#===============================================================================
# Code
#===============================================================================
class LoggerCritical:
    def __enter__(self):
        myLogger = logging.getLogger()
        myLogger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        myLogger = logging.getLogger()
        myLogger.setLevel("DEBUG")
        
class LoggerDebug:
    def __enter__(self):
        myLogger = logging.getLogger()
        myLogger.setLevel("DEBUG")
    def __exit__(self, type, value, traceback):
        myLogger = logging.getLogger()
        myLogger.setLevel("DEBUG")

