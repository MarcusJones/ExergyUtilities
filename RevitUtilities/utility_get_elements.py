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

#-Get objects---
def get_element_by_id(doc,id):
    return doc.GetElement(id)

def get_element_OST_Walls_ActiveView(doc):
    fec = rvt_db.FilteredElementCollector(doc, doc.ActiveView.Id)
    fec.OfCategory(BuiltInCategory.OST_Walls);
    
def get_element_OST_Walls_Document(doc):
    fec = rvt_db.FilteredElementCollector(doc)
    fec.OfCategory(BuiltInCategory.OST_Walls);

def get_grids(doc):
    logging.debug("get_grids")
    # Collect all grids in entire project to a name:element Dict
    collector = FilteredElementCollector(doc)
    collector.OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType()
    collect_grids = collector.ToElements()

    grid_dict = {}

    for grid in collect_grids:
        grid_name = grid.GetParameters('Name')[0].AsString()
        grid_dict[grid_name] = grid
    
    #for k,v in grid_dict.items():
        #    print(k,v)
    logging.debug("Returned {} grids".format(len(grid_dict)))
    return grid_dict

def get_all_views(doc):
    logging.info("{}".format(util.get_self()))
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_dict = dict()
    
    for v in floorplans:
        if not v.IsTemplate:
            #print(v.ViewName,v.ViewType,v.IsTemplate)
            view_dict[v.ViewName] = v

    logging.debug("Returned {} views in dict (no view templates)".format(len(view_dict)))
    
    return view_dict

def get_views_by_type(doc, view_type):

    logging.info("{}".format(util.get_self()))
    floorplans = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    view_dict = dict()
    
    for v in floorplans:
        if not v.IsTemplate and v.ViewType.__str__() == view_type:
            view_dict[v.ViewName] = v

    logging.debug("Returned {} {} in dict (no view templates)".format(len(view_dict), view_type))
    
    return(view_dict)

# def get_all_title_blocks(doc):
#     logging.debug("get_sheet_types")
#     
#     
#     return collector 
#     
def get_title_blocks(doc):
    logging.info("{}".format(util.get_self()))

    this_category = BuiltInCategory.OST_TitleBlocks
    this_class = FamilySymbol
    
    collector = FilteredElementCollector(doc)
    collector.OfCategory(this_category)
    collector.OfClass(this_class)
    
    #collector = get_all_title_blocks(doc)
    
    title_block_dict = dict()
    
    for elem in collector:
        title_block_dict[elem.FamilyName]=elem

    logging.debug("Returned {} title blocks".format(len(title_block_dict)))
    
    return(title_block_dict)



def get_viewports_dict_by_names(doc):
    logging.info("{}".format(util.get_self()))
    fec = FilteredElementCollector(doc)
    
    elem_collection = fec.OfCategory(BuiltInCategory.OST_Viewports).WhereElementIsNotElementType().ToElements()
    
    this_dict = dict()
    for s in elem_collection:
        this_dict[s.Name] = s
        
    #logging.debug("Returned {} floorplans in dict".format(len(view_dict)))
    
    logging.debug("Returned {} in dictionary".format(len(this_dict)))
    
    return this_dict

def get_sheet_dict_by_names(doc):
    logging.info("{}".format(util.get_self()))
    cl_sheets = FilteredElementCollector(doc)
    
    sheets_by_name = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    
    sheet_dict = dict()
    for s in sheets_by_name:
        sheet_dict[s.Name] = s
        
    #logging.debug("Returned {} floorplans in dict".format(len(view_dict)))
    
    logging.debug("Returned {} sheets_by_name in dictionary".format(len(sheets_by_name)))
    
    return sheet_dict

def get_sheets(doc):
    logging.info("{}".format(util.get_self()))
    cl_sheets = FilteredElementCollector(doc)
    
    sheetsnotsorted = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    sheets_by_name = sorted(sheetsnotsorted, key=lambda x: x.SheetNumber)
    
    logging.debug("Found {} sheets_by_name".format(len(sheets_by_name)))
    
    for s in sheets_by_name:
        print(s)
        #print(s.Parameter['Sheet Number'])
        #print(s.Parameter['Sheet Number'].AsString())
        #print('NUMBER: {0}   NAME:{1}'.format(    s.Parameter['Sheet Number'].AsString().rjust(10),
        #                s.Parameter['Sheet Name'].AsString().ljust(50),
        #    ))
        
    return(sheets_by_name)


def get_elements(doc,category):
    #category = BuiltInCategory.OST_Mass
    
    collector = FilteredElementCollector(doc)
    collector.OfCategory(category)
    return collector


#-Get Categories--- 
def get_all_categories(doc):
    categories = doc.Settings.Categories;
    print("{:40} | {:30} | {:30}".format("cat.Name", "cat.Id", "cat.Parent"))    
    for cat in categories:
        print("{:40} | {:30} | {:30}".format(cat.Name, cat.Id, cat.Parent))

def get_elem_BuiltInCategory(doc, elem):
    #print(BuiltInCategory)
    #print_dir(BuiltInCategory)
    #print(BuiltInCategory.GetValues(BuiltInCategory))
    
    
    for i,bic in enumerate(BuiltInCategory.GetValues(BuiltInCategory)):
        print(i,bic, bic.Id)
        
    print("*************")
    #print_dir(bic)
    #print_dir(elem)
    print_dir(elem.Category)
    print("*************")
    
    print_dir(elem.Category.GetCategory(doc, elem.Id))
    #print("*************")
    #print(bic.ToString())
    #print(bic.ToObject())
    #print(bic.ToInt16())
    #print(bic.ToInt64())
    raise

def get_all_BuiltInCategory(elem):
    print(BuiltInCategory)
    raise
    #builtIn = System.Enum.ToObject(BuiltInCategory)
#     for bic in BuiltInCategory.GetValue():
#         print(bic)


#degf





#-BOQ---
def get_sort_all_elements(doc):
    logging.info("{}".format(util.get_self()))
    
    start = time.time()
        
    elements = get_all_elements(doc)
    
    element_dict = defaultdict(list)
    
    for el in elements:
        this_cat = el.Category
        if this_cat:
            this_cat_name = this_cat.Name
            element_dict[this_cat_name].append(el)
            
    #for k in element_dict:
    #    print("{} contains {} elements".format(k, len(element_dict[k])))
        
    end = time.time()
        
    logging.info("Returned element dictionary with {} categories of {} in time: {}s".format(len(element_dict), len(elements),end - start))
    
    return element_dict


def get_sort_all_FamilyInstance(doc):
    logging.info("{}".format(util.get_self()))
    
    start = time.time()
        
    elements = get_all_FamilyInstance(doc)
    
    element_dict = defaultdict(list)
    
    for el in elements:
        this_cat = el.Category
        if this_cat:
            this_cat_name = this_cat.Name
            element_dict[this_cat_name].append(el)
         
    #for k in element_dict:
    #    print("{} contains {} elements".format(k, len(element_dict[k])))
        
    end = time.time()
        
    logging.info("Returned element dictionary with {} categories of {} in time: {}s".format(len(element_dict), len(elements),end - start))
    
    return element_dict

def get_linear_MEP(doc):
    # Now, add (logical OR) additionally the MEP classes (which are not categories!)
    mep_class_filters = list()
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.CableTray))
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.Wire))
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.Conduit))
    mep_class_filters.append(ElementClassFilter(rvt_db.Mechanical.Duct))
    mep_class_filters.append(ElementClassFilter(rvt_db.Plumbing.Pipe))

    merged_filter = LogicalOrFilter(mep_class_filters)

    elements = FilteredElementCollector(doc).WherePasses(merged_filter).ToElements()

    logging.info("Returning {} elements ".format(len(elements)))
    
    return elements
    
def get_BOQ_elements(doc):
    
    # General categories
    cat_filters = list()
    for this_bic in util.REVIT_CATEGORIES_BIC:
        cat_filters.append(ElementCategoryFilter(this_bic))
        
    # This selects all elements in the Built-Ins
    filter_over_cats = LogicalOrFilter(cat_filters)
    
    # From the Built-Ins, make sure we only take the Instances
    filter_cats_instances = LogicalAndFilter(filter_over_cats,ElementClassFilter(FamilyInstance)) 

    # Now, add (logical OR) additionally the MEP classes (which are not categories!)
    mep_class_filters = list()
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.CableTray))
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.Wire))
    mep_class_filters.append(ElementClassFilter(rvt_db.Electrical.Conduit))
    mep_class_filters.append(ElementClassFilter(rvt_db.Mechanical.Duct))
    mep_class_filters.append(ElementClassFilter(rvt_db.Plumbing.Pipe))

    merged_filter = LogicalOrFilter([filter_cats_instances]+mep_class_filters)
    
    elements = FilteredElementCollector(doc).WherePasses(merged_filter).ToElements()
    
    logging.info("Returning {} elements over {} Built-In-Categories and {} classes".format(len(elements),
                                                                            len(util.REVIT_CATEGORIES_BIC),
                                                                            len(mep_class_filters),
                                                                            ))
    
    return elements

def get_all_MEP_elements(doc):
    
    systems_list = FilteredElementCollector(doc).OfClass( MEPSystem ).ToElements()
    
    all_elements = list()
    for i, sys in enumerate(systems_list):
        
        #print(i,sys,sys.Name)
        
        #print(type(sys),"=", rvt_db.Plumbing.PipingSystem)
        
        # Skip the spares and spaces in a DB
        if type(sys) == rvt_db.Electrical.ElectricalSystem:
            if str(sys.CircuitType) == "Spare":
                continue
            if str(sys.CircuitType) == "Space":
                continue
        # Just checking
        if type(sys) == rvt_db.Plumbing.PipingSystem:
            pass 

                    
        for el in sys.Elements:
            #print("\t\t",el.Name)
            
            try:
                these_elems = sys.Elements
            except:
                logging.error("Trying access to elements in system {} {}".format(sys,sys.Name))
                #print(sys.CircuitNumber)
                #print(sys.CircuitType)
                raise
        all_elements.append(these_elems)
        
    logging.info("Returning {} MEP elements".format(len(all_elements)))
    
    return all_elements



def get_all_MEP_element_IDs(doc):

    systems_list = FilteredElementCollector(doc).OfClass( MEPSystem ).ToElements()
    
    all_elements = list()
    for i, sys in enumerate(systems_list):
        
        #print(i,sys,sys.Name)
        
        #print(type(sys),"=", rvt_db.Plumbing.PipingSystem)
        
        # Skip the spares and spaces in a DB
        if type(sys) == rvt_db.Electrical.ElectricalSystem:
            if str(sys.CircuitType) == "Spare":
                continue
            if str(sys.CircuitType) == "Space":
                continue
        # Just checking
        if type(sys) == rvt_db.Plumbing.PipingSystem:
            pass 

                    
        for el in sys.Elements:
            #print("\t\t",el.Name)
            
            try:
                these_elems = sys.Elements
            except:
                logging.error("Trying access to elements in system {} {}".format(sys,sys.Name))
                #print(sys.CircuitNumber)
                #print(sys.CircuitType)
                raise
            
            
            all_elements.append(el.Id)
        
    logging.info("Returning {} MEP element IDs".format(len(all_elements)))
    
    return all_elements

def get_all_FamilyInstance(doc):
    """
    Returns FamilyInstance objects only.
    """
    logging.info("{}".format(util.get_self()))
    
    this_filter = rvt_db.LogicalOrFilter(
      rvt_db.ElementIsElementTypeFilter( False ), 
      rvt_db.ElementIsElementTypeFilter( True ) 
      )
    
    elements = FilteredElementCollector(doc).WherePasses( this_filter).OfClass(FamilyInstance).ToElements()
    
    logging.info("Returning {} elements".format(len(elements)))
    
    return elements


def get_all_elements_IDs(doc):
    """
    Returns FamilySymbol, FamilyInstance, ALL, etc.
    """
    logging.info("{}".format(util.get_self()))
    
    this_filter = rvt_db.LogicalOrFilter(
      rvt_db.ElementIsElementTypeFilter( False ), 
      rvt_db.ElementIsElementTypeFilter( True ) 
      )
    
    element_ids = FilteredElementCollector(doc).WherePasses( this_filter).ToElementIds()
    
    logging.info("Returning {} element IDs".format(len(element_ids)))
    
    return element_ids

def get_all_elements_IDs_Filter(doc):
    """
    System.Diagnostics.Stopwatch watch = new System.Diagnostics.Stopwatch();
watch.Restart();
 
IList<Element> elements = new List<Element>();
FilteredElementCollector finalCollector = new FilteredElementCollector(CachedDoc);
 
finalCollector.WherePasses(
    new LogicalOrFilter(
        new List<ElementFilter>
        {
            new ElementCategoryFilter(BuiltInCategory.OST_Doors),
            new ElementCategoryFilter(BuiltInCategory.OST_Windows),
            new ElementCategoryFilter(BuiltInCategory.OST_CeilingOpening),
            new ElementCategoryFilter(BuiltInCategory.OST_FloorOpening),
            new ElementCategoryFilter(BuiltInCategory.OST_RoofOpening)
        }));
 
elements = finalCollector.ToElements();
 
watch.Stop();
using (StreamWriter sw = new StreamWriter(@"c:\temp\Output.txt", true))
{
    sw.WriteLine(string.Format("{0} doors/windows/openings were found in {1} milli-seconds.", elements.Count, watch.Elapsed.Milliseconds));
}
    """
    logging.info("{}".format(util.get_self()))
    
    this_filter = rvt_db.LogicalOrFilter(
      rvt_db.ElementIsElementTypeFilter( False ), 
      rvt_db.ElementIsElementTypeFilter( True ) 
      )
    
    element_ids = FilteredElementCollector(doc).WherePasses( this_filter).OfCategory().ToElementIds()

    logging.info("Returning {} element IDs".format(len(element_ids)))
    
    return element_ids


def get_all_elements(doc, ):
    """
    Returns FamilySymbol, FamilyInstance, ALL, etc.
    """
    logging.info("{}".format(util.get_self()))
    
    this_filter = rvt_db.LogicalOrFilter(
      rvt_db.ElementIsElementTypeFilter( False ), 
      rvt_db.ElementIsElementTypeFilter( True ) 
      )
    
    elements = FilteredElementCollector(doc).WherePasses( this_filter).ToElements()
    
    logging.info("Returning {} elements".format(len(elements)))
    
    return elements
