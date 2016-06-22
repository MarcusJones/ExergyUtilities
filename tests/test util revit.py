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
