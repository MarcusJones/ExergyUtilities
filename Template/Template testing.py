"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:

from config import *

import logging.config
import unittest


from utility_inspect import get_self
from utilities_xml import get_table_all_names, print_table
from idf_parser import IDF
import os.path as path

#===============================================================================
# Logging
#===============================================================================
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    this_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))

import unittest

# Logging
import logging
logging.basicConfig(format='%(funcName)-20s %(levelno)-3s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    this_path = path.dirname(path.dirname(path.abspath(__file__)))
    sys.path.append(this_path)
    logging.debug("ADDED TO PATH: ".format(this_path))



# External 
#import xxx

# Own
from ExergyUtilities.utility_inspect import get_self, get_parent

#===============================================================================
# Testing
#===============================================================================
class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        self.curr_dir = os.path.dirname(os.path.realpath(__file__))
        
    def test010_empty(self):
        print("**** TEST {} ****".format(get_self()))
