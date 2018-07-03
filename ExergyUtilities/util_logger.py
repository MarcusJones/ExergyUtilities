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
        my_logger = logging.getLogger()
        my_logger.setLevel("CRITICAL")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")


class LoggerCritical:
    def __enter__(self):
        my_logger = logging.getLogger()
        #my_logger.setLevel("CRITICAL")
        logger.setLevel(logging.DEBUG)
        return self
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")

class NoLog:
    def __enter__(self):
        logging.disabled = True
    def __exit__(self, type, value, traceback):
        logging.disabled = False    


#import requests
import logging
for key in logging.Logger.manager.loggerDict:
    print(key)

logging.getLogger("github.Requester").setLevel(logging.WARNING)

        
class LoggerDebug:
    def __enter__(self):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")
    def __exit__(self, type, value, traceback):
        my_logger = logging.getLogger()
        my_logger.setLevel("DEBUG")

