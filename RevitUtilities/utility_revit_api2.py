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

import utility as util 

def family_data_dict(doc,fam):
    assert type(fam) == rvt_db.FamilyInstance, "Not an instance"
    data = dict()

    data["Name"] = fam.Name
    
    #if fam.GetTypeId():
    #    fam_type = doc.GetElement(fam.GetTypeId())
    #    print(fam_type)
    #    type_name = fam_type.Name.ToString()
    #else:
    #    type_name = "DNE"
    
    data["Type"] = fam.Symbol.ToString()
    
    data["Family"] = fam.Symbol.FamilyName
    return data

def select_instances_by_type_id(doc, type_id):
    this_filter = FamilyInstanceFilter(doc, type_id)
    elems = FilteredElementCollector(doc).WherePasses(this_filter).ToElements()
    return elems

    #return [el for el in elems]
    


#-Family---


def get_type(this_elem):
    raise
    this_elem.GetType() # For floorplans!


def set_instance_param(doc, category = BuiltInCategory.OST_Mass, inst_name = 'BoxFamily'):
    t = Transaction(doc, 'Modify existing family instances.')
     
    t.Start()
     
    collector = FilteredElementCollector(doc)
    collector.OfCategory(category)
    collector.OfClass(FamilyInstance)
     
    famtypeitr = collector.GetElementIdIterator()
    famtypeitr.Reset()
     
    inc = 1
     
    for famtypeID in famtypeitr:
        faminst = doc.get_Element(famtypeID)
     
        if faminst.Name == inst_name:
            param = faminst.get_Parameter('height')
            param.Set(2*inc)
            inc = inc + 1
     
    t.Commit()

def collector_category_class(doc):
    pass

def get_family():
    pass



def get_element_from_id(doc, id_int):

    elem_id = rvt_db.ElementId(id_int)
    elem = doc.GetElement(elem_id)
    
    return elem


#-Selection---
def selection(uidoc,doc):
    logging.debug(util.get_self())
    #print(uidoc.Selection)
    for el_ID in uidoc.Selection.GetElementIds():
        el = doc.GetElement(el_ID)
        logging.debug("Selected: {} {}".format(el_ID,el))        
    
def single_selection(uidoc,doc):
    logging.debug(util.get_self())
    selection = uidoc.Selection.GetElementIds()
    assert len(selection) == 1, "*Must select one and only one element*"
    for el_ID in selection:
        el = doc.GetElement(el_ID)
    logging.debug("Returning element: {} {}".format(el_ID,el))                
    return el

def inspect_selection(el):
    print("Name {}".format(el.Name))
    print("GetType {}".format(el.GetType()))
    print("GetTypeId {}".format(el.GetTypeId()))
    print("Parameter {}".format(el.Parameter))
    print("Parameters {}".format(el.Parameters))
    print("ParametersMap {}".format(el.ParametersMap))    
    
    print("GetOrderedParameters {}".format(el.GetOrderedParameters()))
    print("GetParameters {} -NEEDS PARAM NAME- ".format(el.GetParameters))

