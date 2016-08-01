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

#-XXX---

def parameter_exists(el, param_name):
    #if p in el.Parameters: return True
    #else: return False
    for p in el.Parameters:
        if p.Definition.Name == param_name:
            return True
    return False

def get_parameter_value_float(el, param_name, flg_DNE=False):
    flg_found = False
    for p in el.Parameters:
        if p.Definition.Name == param_name:
            p_val = p.AsDouble()
            flg_found = True
            #this_name = p.AsString()
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,p.AsString()))
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,this_name))
            break
    
    if flg_found:
        return p_val
    elif not flg_found and flg_DNE:
        return "DNE"
    else:
        print("Can't find this parameter:")
        print(el, el.Name, param_name, flg_DNE)
        raise
    #return_str = p.AsString()
    #print("Returning {}")
    #return p_val
#        p.Definition.Name AsString 


def get_parameter_value_str(el, param_name, flg_DNE=False):
    flg_found = False
    for p in el.Parameters:
        if p.Definition.Name == param_name:
            p_val = p.AsValueString()
            flg_found = True
            #this_name = p.AsString()
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,p.AsString()))
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,this_name))
            break
    
    if flg_found:
        return p_val
    elif not flg_found and flg_DNE:
        return "DNE"
    else:
        print("Can't find this parameter:")
        print(el, el.Name, param_name, flg_DNE)
        raise
    #return_str = p.AsString()
    #print("Returning {}")
    #return p_val
#        p.Definition.Name AsString 


def get_parameter_value(el, param_name, flg_DNE=False):
    
    
    flg_found = False
    for pi in el.Parameters:
        if pi.Definition.Name == param_name:
            p_val = pi.AsString()
            flg_found = True
            #this_name = p.AsString()
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,p.AsString()))
            #print("{} matches {} = {}".format(p.Definition.Name,param_name,this_name))
            break
    
    
    if not flg_found and type(el) == FamilyInstance:
        for pf in el.Symbol.Parameters:
            if pf.Definition.Name == param_name:
                p_val = pf.AsString()
                flg_found = True
                break
            
    if not flg_found and type(el) == FamilyInstance:
        for pf in el.Symbol.Family.Parameters:
            if pf.Definition.Name == param_name:
                p_val = pf.AsString()
                flg_found = True
                break
        
    if flg_found:
        if p_val == None:
            return ""
        else:
            return p_val
        
    elif not flg_found and flg_DNE:
        return "DNE"
    else:
        logging.error("Parameter {} not found in {} {} not found".format(param_name,el, el.Name, flg_DNE))
        #print()
        raise
    #return_str = p.AsString()
    #print("Returning {}")
    #return p_val
#        p.Definition.Name AsString 

def change_parameter(doc, el, param_name, new_value, verbose = True):
    
    logger = logging.getLogger()
    
    if not verbose:
        logger.setLevel(logging.INFO)
    
    target_param = None
    for p in el.Parameters:
        #print(p.Definition.Name)
        if p.Definition.Name == param_name:
            target_param = p
            break
    
    if not target_param:
        print(el)
        print(el.Name)
        print("{} not found".format(param_name))
        table_parameters(el)
        raise
    
    #assert target_param, 
    
    this_type = target_param.Definition.ParameterType
    target_type = rvt_db.ParameterType.Text
    assert this_type == target_type, "This function only works {}, not {}".format(target_type,this_type)

    with Trans(doc, "Change param {} to {}".format(param_name,new_value)):
        target_param.Set(new_value)
    
            
    
    logging.debug("Overwrite {} from {} to {} in ".format(target_param.Definition.Name,
                                                    target_param.AsString(),
                                                    new_value,
                                                    target_param.Element))
      
    logger.setLevel(logging.DEBUG)



def change_parameter_multiple(doc, el_list, param_name, new_value_list):
    #doc
    #el_list : N Elements
    #param_name : One parameter at a time
    #new_value_list : N New values

    #logging.debug("Overwriting {} {} parameters in {} elements".format(len(new_value_list),param_name,len(el_list)))

    logger = logging.getLogger()

    target_param_list = list()
    for el in el_list:
        target_param = None
        
        # Get the parameter
        for p in el.Parameters:
            #print(p.Definition.Name)
            if p.Definition.Name == param_name:
                target_param = p
                break
        
        # Ensure that it exists
        if not target_param:
            print(el)
            print(el.Name)
            print("{} not found".format(param_name))
            table_parameters(el)
            raise
        
        # Assert that the parameter is TEXT
        this_type = target_param.Definition.ParameterType
        target_type = rvt_db.ParameterType.Text
        assert this_type == target_type, "This function only works {}, not {}".format(target_type,this_type)
        
        # Add this parameter
        target_param_list.append(target_param)
    
    # Built the changes, now commit all
    logger.setLevel(logging.INFO)
    with Trans(doc, "Change param".format()):
        for target_param, new_value in zip(target_param_list, new_value_list):
            target_param.Set(new_value)
    
    logger.setLevel(logging.DEBUG)
        
    logging.debug("Overwrote {} {} parameters in {} elements".format(len(new_value_list),param_name,len(el_list)))
          
        
def table_parameters(el):
    
    logging.debug(util.get_self())

    print("{:20}".format("-name-").encode('utf-8'), end="")
    print("{:20}".format("-ParameterGroup-").encode('ascii'), end="")
    print("{:30}".format("-ParameterType-").encode('ascii'), end="")
    print("{:30}".format("-Value String-").encode('ascii'), end="")
    print("{:30}".format("-String-").encode('ascii'), end="")
    print("{:30}".format("-UnitType-").encode('ascii'), end="")
    print("")

    for param in el.Parameters:
        print("{0!s:20}".format(param.Definition.Name), end="")
        print("{0!s:20}".format(param.Definition.ParameterGroup), end="")
        print("{0!s:30}".format(param.Definition.ParameterType), end="")
        print("{0!s:30}".format(param.AsValueString()), end="")
        print("{0!s:30}".format(param.AsString()), end="")
        print("{0!s:30}".format(param.Definition.UnitType), end="")
        print("")

def all_params(el):
    for param in el.Parameters:
        print(param.Definition.Name, ":", param.AsValueString())
        
def list_parameters(el):
    logging.debug(util.get_self())
    for param in el.Parameters:
        print("Definition: {}".format(param.Definition))
        print("Definition.Name: {}".format(param.Definition.Name))        
        print("Definition.ParameterGroup: {}".format(param.Definition.ParameterGroup))        
        print("Definition.ParameterType: {}".format(param.Definition.ParameterType))        
        print("Definition.UnitType: {}".format(param.Definition.UnitType))
        
        print("param.AsString(): {}".format(param.AsString()))
        print("param.AsValueString(): {}".format(param.AsValueString()))
        print("param.AsElementId(): {}".format(param.AsElementId()))
        
        print("param: {}".format(param))
        #print("DisplayUnitType: {}".format(param.DisplayUnitType))
        print("Element: {}".format(param.Element))
        #print("GUID: {}".format(param.GUID))
        print("HasValue: {}".format(param.HasValue))
        print("Id: {}".format(param.Id))
        print("IsReadOnly: {}".format(param.IsReadOnly))
        print("IsShared: {}".format(param.IsShared))
        print("StorageType: {}".format(param.StorageType))

def project_parameters(doc):

    pm = doc.ParameterBindings
    it = pm.ForwardIterator()
    it.Reset()
    
    deflist = []
    paramidlist = set()
    while(it.MoveNext()):
        p = it.Key
        b = pm[ p ]
    
        if isinstance(b, rvt_db.InstanceBinding):
            bind = 'Instance'
        elif isinstance(b, rvt_db.TypeBinding):
            bind = 'Type'
        else:
            bind = 'Unknown'
    
        print('\n')
        print('-'*100)
        print('PARAM: {0:<30} UNIT: {1:<10} TYPE: {2:<10} GROUP: {3:<20} BINDING: {4:<10} VISIBLE: {6}\nAPPLIED TO: {5}\n'.format(
                p.Name,
                str(p.UnitType),
                str(p.ParameterType),
                str(p.ParameterGroup),
                bind,
                [cat.Name for cat in b.Categories],
                p.Visible
                ))
        deflist.append( p )



def document_parameters(doc):
    logging.debug(util.get_self())
    params = FilteredElementCollector(doc).OfClass(rvt_db.ParameterElement)
#   filteredparams = []
    
    for param in params:
#        #Store parameters which has a name starting with "magi" or "MC"
#         if param.Name.startswith(("magi", "MC")): #startswith method accept tuple
#             filteredparams.append(param)            
        print(param.Name)

