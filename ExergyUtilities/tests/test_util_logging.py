"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:


import unittest

# Logging
import logging
logging.basicConfig(format='%(funcName)-20s %(levelno)-3s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")


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
