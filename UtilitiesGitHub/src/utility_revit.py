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
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest
from win32com.client import Dispatch
import clr
#from Autodesk.Revit.DB import *
from utility_inspect import whoami, whosdaddy, listObject
import sys

sys.path.append(r'D:\Apps\Autocad Plant 3D\Revit 2015')

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUIMacros')
import Autodesk.Revit.DB as rdg
#from Autodesk.Revit.DB.Architecture import *
#from Autodesk.Revit.DB.Analysis import *

print(rdg)
print(dir(rdg))
print(rdg.__doc__)
print(rdg.__name__)
print(rdg.__file__)

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
selection = list(__revit__.ActiveUIDocument.Selection.Elements)

#===============================================================================
# Code
#===============================================================================
class MyClass(object):
    """This class does something for someone.
    """
    def __init__(self, aVariable):
        pass

class MySubClass(MyClass):
    """This class does

    """
    def __init__(self, aVariable):
        super(MySubClass,self).__init__(aVariable)
    def a_method(self):
        """Return the something to the something."""
        pass

def some_function():
    """Return the something to the something."""
    pass

#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))
        #print(clr.FindAssembly('RevitAPIUI'))
        uidoc = __revit__.ActiveUIDocument
        raise
        
        #import Autodesk.Revit.DB as rdb
        #import Autodesk.Revit.DB as rdb
        #print(dir(rdb))
        
        
        #clr.AddReference('RevitAPIUI')
        #sys.path.append(r'D:\Apps\Autocad Plant 3D\Revit 2015')
        #clr.AddReference('RevitAPIUI')
        #rvt = 
        #print(rvt)
        #print(clr.AddReference('RevitAPIUI'))

        #print(clr)
        #TaskDialog.Show("Revit","jj")
        #print(clr.AddReferenceToFileAndPath(r'D:\Apps\Autocad Plant 3D\Revit 2015\RevitAPI.dll'))
        #uidoc = __revit__.ActiveUIDocument
        #doc = __revit__.ActiveUIDocument.Document
        #selection = list(__revit__.ActiveUIDocument.Selection.Elements)

        
        #print(clr.a(r'D:\Apps\Autocad Plant 3D\Revit 2015\RevitAPI'))
        #print(clr.AddReference('RevitAPI'))

        print(clr.FindAssembly('RevitServices'))
        

        #clr.AddReference('RevitAPIUI')
        #rvt = Dispatch('Revit.exe')

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
