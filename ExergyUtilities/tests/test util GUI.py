"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
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
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):
    
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

    @unittest.skip("")         
    def test020_SimpleCreation(self):
        print "**** TEST {} ****".format(whoami())
        print "BETTER?"
        ret = simpleYesNo("Test")
        print "Got  answer;", ret

    @unittest.skip("")         
    def test030_getDir(self):
        print "**** TEST {} ****".format(whoami())
        app = wx.App(False)
        frame = MyForm()
        frame.Show()
        app.MainLoop()

    def test040_getDirFOrm(self):

        print "**** TEST {} ****".format(whoami())
        

        def testFunction1(dirName):
            print "Test function RUN"
            print dirName
        
        runDirFilter(testFunction1)

    def test050_simple_text(self):
        simple_text("test")
        
