RevitPath = r"C:\Program Files\Autodesk\Revit 2017"
import sys
sys.path.append(RevitPath)
import clr

clr.AddReference('RevitAPI')


#----- Try

from Autodesk.Revit.DB import Element, ChangePriority, SubTransaction
from Autodesk.Revit.DB import IUpdater, UpdaterId, UpdaterRegistry
from Autodesk.Revit.DB.Architecture import RoomFilter
#from Autodesk.Revit.UI import TaskDialog
from System import Guid

app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document





#----- This works but not for active object?

# Add DB UI Import to globals so it can be imported by rpw
clr.AddReference('RevitAPI')
#clr.AddReference('RevitAPIUI')
from Autodesk.Revit import DB, UI
#globals().update({'DB': DB, 'UI': UI})


doc = DB.Document


params = DB.FilteredElementCollector(doc).OfClass(DB.ParameterElement)
#   filteredparams = []

for param in params:
#        #Store parameters which has a name starting with "magi" or "MC"
#         if param.Name.startswith(("magi", "MC")): #startswith method accept tuple
#             filteredparams.append(param)            
    print(param.Name)




print(DB)
print(UI)

#print(__revit__)
#print(UI.ActiveUIDocument)
#import Autodesk.Revit.UI as UI

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

print(FilteredElementCollector)

#     # Replace Globals with Mock Objects for Sphinx and ipy direct exec.
#     logger.warning('RevitAPI References could not be added')
#     from rpw.utils.sphinx_compat import MockObject
#     globals().update({'DB': MockObject(fullname='Autodesk.Revit.DB'),
#                       'UI': MockObject(fullname='Autodesk.Revit.DB')})
#     uiapp = MockObject(fullname='Autodesk.Revit.UI.UIApplication')
#     _host = None




# try:
#     self.uiapp = __revit__
#     self._host = Revit.HOSTS.RPS
# except NameError:
#     try:
#         # Try Getting handler from Dynamo RevitServices
#         self.uiapp = self.find_dynamo_uiapp()
#         self._host = Revit.HOSTS.DYNAMO
#     except Exception as errmsg:
#         logger.warning('Revit Application handle could not be found')



raise





import math

#RevitAPIdll= r"C:\Program Files\Autodesk\Revit 2017\RevitAPI"
#RevitAPIUIdll= r"C:\Program Files\Autodesk\Revit 2017\RevitAPIUI"





#clr.AddReference(RevitAPIdll)
#clr.AddReference(RevitAPIUIdll)

clr.AddReference('RevitAPI')
#clr.AddReference('RevitAPIUI')
from Autodesk.Revit import DB, UI

#raise

#===============================================================================
# pyRevit
#===============================================================================
__doc__ = 'Script docstring'

#===============================================================================
# Logging
#===============================================================================
import logging
logging.basicConfig(level=logging.DEBUG)

#===============================================================================
# Import Revit
#===============================================================================
rvt_app = __revit__.Application
#rvt_uidoc = __revit__.ActiveUIDocument
#rvt_doc = __revit__.ActiveUIDocument.Document
import Autodesk.Revit.DB as rvt_db

#===============================================================================
# Imports other
#===============================================================================
import sys
from collections import defaultdict

path_package = r"C:\EclipseGit\ExergyUtilities\RevitUtilities"
sys.path.append(path_package)
#import utility_revit_api2 as util_ra
#import utility as util

#===============================================================================
# Definitions
#===============================================================================


#===============================================================================
# Main
#===============================================================================
#-Logging info---
logging.info("Python version : {}".format(sys.version))
logging.info("uidoc : {}".format(rvt_uidoc))
logging.info("doc : {}".format(rvt_doc))
logging.info("app : {}".format(rvt_app))

#-Paths---
folder_csv = r"C:\CesCloud Revit\_03_IKEA_Working_Folder"
name_csv = r"\20160729 Document Register.csv"
path_csv = folder_csv + name_csv

#-Get data---
#data_dict = util.get_data_csv(path_csv)
#data_dict_RVT = [row for row in data_dict if row['SOURCE'] == 'RVT']

#-Get all floorplans, sheets_by_name, titleblocks, legends---
util_ra.get_all_views(rvt_doc)
title_blocks = util_ra.get_title_blocks(rvt_doc)
sheets_by_name = util_ra.get_sheet_dict_by_names(rvt_doc)
floorplans = util_ra.get_views_by_type(rvt_doc, 'FloorPlan')
all_views = util_ra.get_all_views(rvt_doc)
legends = util_ra.get_views_by_type(rvt_doc,'Legend')
templates = util_ra.get_view_templates(rvt_doc)

#-Check---
#check_sheets(data_dict_RVT,sheets_by_name,all_views,templates)

logging.info("---DONE---".format())