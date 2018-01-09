"""This module does blah blah."""
from __future__ import print_function

#===============================================================================
# Import Revit
#===============================================================================
# import Autodesk.Revit.DB as rvt_db
# from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
# from Autodesk.Revit.DB import FamilyInstanceFilter, ElementCategoryFilter, ElementClassFilter
# from Autodesk.Revit.DB import LogicalAndFilter, LogicalOrFilter
# from Autodesk.Revit.DB import FamilyInstance, FamilySymbol
# from Autodesk.Revit.DB import Transaction
# from Autodesk.Revit.DB import Line, XYZ, CurveLoop
# from Autodesk.Revit.DB import MEPSystem

try:
    import Autodesk.Revit.DB as rvt_db
    from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
    from Autodesk.Revit.DB import FamilyInstanceFilter, ElementCategoryFilter, ElementClassFilter
    from Autodesk.Revit.DB import LogicalAndFilter, LogicalOrFilter
    from Autodesk.Revit.DB import FamilyInstance, FamilySymbol
    #from Autodesk.Revit.DB import Transaction
    from Autodesk.Revit.DB import Line, XYZ, CurveLoop
    from Autodesk.Revit.DB import MEPSystem
except:
    pass

#===============================================================================
# Import Python
#===============================================================================
#import System
#import inspect
#import csv
from collections import defaultdict
import time
import logging
#from operator import itemgetter

import utility_general as util 


#-XXX---

    
def create_dependent(doc, active_view, part_name):
    # Copy current view as dependant\
    logging.debug("create_dependent".format())
    with Trans(doc, "Duplicate"):
        new_view_id = active_view.Duplicate(rvt_db.ViewDuplicateOption.AsDependent)
        new_view = doc.GetElement(new_view_id)
    
    new_name = new_view.Name.replace("Dependent 1", part_name)

    with Trans(doc, "Rename"):
        new_view.Name = new_name
    
    logging.debug("Created {}".format(new_view.Name))
    return new_view

def rename_sheets(data_dict, sheets_by_name):
    raise "OBSELETE SEE CREATE SHEETS"    
    """
    logging.debug(util_ra.util.get_self())
    
    for i,row in enumerate(data_dict):
        assert row['SOURCE'] == 'RVT', "Only works with RVT drawings, not [{}]".format(row['SOURCE'])
        if row['OLD NAME']:
            assert row['OLD NAME'] in sheets_by_name, "{} sheet not found in project".format(row['OLD NAME'])
        else:
            continue
        
        this_sheet = sheets_by_name[row['OLD NAME']]
        
        # Change OLD NAME to Sheet Name column
        util_ra.change_parameter(rvt_doc, 
                                 this_sheet, 
                                 'Sheet Name', 
                                 row['Sheet Name'])
        
        # Change OLD NUMBER to Sheet Number column
        util_ra.change_parameter(rvt_doc, 
                                 this_sheet, 
                                 'Sheet Number', 
                                 row['Sheet Number'])        
        
        logging.debug("Updated {}".format(row['OLD NAME']))
    """

def create_sheet(doc, title_block, number, name):
    logging.info("{}".format(util.get_self()))
    
    title_block_id = title_block.Id
    with Trans(doc, "Create sheet {} {}".format(number,name)):
        new_sheet = rvt_db.ViewSheet.Create(doc, title_block_id)
        new_sheet.Name = name
        new_sheet.SheetNumber = number
        
    return new_sheet

    
    
    """
     Code Region: ViewSheet.Create()

    public static ViewSheet ViewSheet.Create(Document document, ElementId titleBlockTypeId);

    The newly created sheet has no floorplans. The Viewport.Create() method is used to add floorplans. 
    The Viewport class is used to add regular floorplans to a view sheet, i.e. plan, elevation, 
    drafting and three dimensional. To add schedules to a view, use ScheduleSheetInstance.Create() instead. 
    """
    
    #print(ViewSheet)
#     rvt_db.View#
#     
#     title_blocks = rvt_doc.TitleBlocks;
#     if (lend(title_blocks) == 0):
#         raise(Exception("No title blocks"))
#     
#     print(title_blocks)
    
    # Copy current view as dependant
    #t = Transaction(doc, 'This is my new transaction')
    #t.Start()
    #new_view_id = active_view.Duplicate(ViewDuplicateOption.AsDependent)
    #new_view = doc.GetElement(new_view_id)
    #t.Commit()
    
    #new_name = new_view.Name.replace("Dependent 1", part_name)
    
    #t.Start()
    #new_view.Name = new_name
    #t.Commit()




#-Views and Sheets---
def get_view_templates(doc):
    logging.info("{}".format(util.get_self()))
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_template_dict = dict()
    
    for v in floorplans:
        if v.IsTemplate:
            view_template_dict[v.ViewName] = v
  
    logging.debug("Returned {} view templates in dict".format(len(view_template_dict)))
    
    return view_template_dict    

def apply_template(doc, view):
    pass
#     
#     View viewTemplate = (from v in new FilteredElementCollector(doc)
#         .OfClass(typeof(View))
#         .Cast<View>()
#         where v.IsTemplate == true && v.Name == "MyViewTemplate"
#         select v)
#         .First();
# 
#     using (Transaction t = new Transaction(doc,"Set View util_python_path"))
#     {
#         t.Start();           
#         doc.ActiveView.ViewTemplateId = viewTemplate.Id;
#         t.Commit();
#     }
# }    



# def print_title_blocks(doc):
#     
#     collector = get_all_title_blocks(doc)
#     #collector.ToElements()
#     #elem_list = [el for el in collector]
#     #logging.debug("{} elements".format(len(elem_list)))
# 
#     print("{:30} | {:30} |".format("Name:","ID:"))
#     for elem in collector:
#         print("{:30} | {:30} ".format(elem.FamilyName,elem.Id))
#     
    #for item in dir(elem):
    #    print(item)
        #print(elem.Name)
        #print(dir(elem))
    #print(elems)
    
    #raise
#     print(dir(collector))
#     
#     print(len(collector))
#     
#     
#     
#     for elem in collector.GetElementIterator():
#         print(elem)
#         print(elem.Name)
    
    
    #print(collector.ToList())

def add_view_sheet(doc, sheet, view, center_pt, viewport_ID=False):
    """
    
    Add a view object to a sheet object given the center_pt
    sheet : Autodesk.Revit.DB.ViewSheet
    view : Autodesk.Revit.DB.ViewPlan 
    center_pt: 
    """
    logging.info("{}".format(util.get_self()))
    
    #print(sheet)
    #print(view)
    #print(center_pt)
    
    with Trans(doc, "Add view to sheet"):
        view_port = rvt_db.Viewport.Create(doc, sheet.Id, view.Id, center_pt)
        
        if viewport_ID:
            #print(viewport_ID)
            view_port.ChangeTypeId(viewport_ID)

    
    logging.debug("View {} placed on sheet {} {} at {}".format(view.Name, sheet.Name, sheet.SheetNumber, center_pt))
    return view_port
