#===============================================================================
#--- SETUP Config
#===============================================================================
#from config.config import *
#import unittest
from __future__ import print_function
#===============================================================================
#--- SETUP Logging
#===============================================================================
#import logging.config
#print(ABSOLUTE_LOGGING_PATH)
#logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
#myLogger = logging.getLogger()
#myLogger.setLevel("DEBUG")
#logging.debug("HI")
#print("HI")

import logging
logging.warning('Watch out!') # will print a message to the console
logging.info('I told you so') # will not print anything

#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
import time
from collections import defaultdict
#import pandas as pd
import csv

#===============================================================================
#--- SETUP external modules
#===============================================================================
try:
    import Autodesk.Revit.DB as rvt_db
    #from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
    #from Autodesk.Revit.DB import FamilyInstanceFilter, ElementCategoryFilter, ElementClassFilter
    #from Autodesk.Revit.DB import LogicalAndFilter, LogicalOrFilter
    #from Autodesk.Revit.DB import FamilyInstance, FamilySymbol
    #from Autodesk.Revit.DB import Transaction
    #from Autodesk.Revit.DB import Line, XYZ, CurveLoop
    #from Autodesk.Revit.DB import MEPSystem
except:
    pass

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
#from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================
def mlog(this_str):
    print("LOG: ", this_str)
    
def start():
    mlog("J")

def run():
    pass

def write_dictoflists(fname, this_dict):
    
    #df = pd.DataFrame.from_dict(this_dict, orient='columns', dtype=None)
    #print(df)
    #print(df.shape)

    
    line = 0
    with open(fname, "wb") as outfile:

        #writer = csv.writer(outfile, delimiter = "\t")
        writer = csv.writer(outfile, delimiter = ";")
        #writer = csv.writer(outfile)
        
        #keys = sorted(this_dict.keys())
        #keys = [i.encode('utf-8', 'ignore').strip() if i else "" for i in keys]
        
        new_dict = dict()
        for k in this_dict:
            nkey = k.encode('utf-8','ignore')
            new_dict[nkey] = this_dict[k]
            
        keys = sorted(new_dict.keys())
        
        writer.writerow(keys)
        mlog("Wrote head to {}".format(fname))
        #writer.writerows(zip(*[this_dict[key].encode('utf-8') for key in keys]))
        
        for row in zip(*[new_dict[key] for key in keys]):
            line += 1
            #print("LINE: ",line)            
            #print(row)
            #for i in row:
            row2 = [i.encode('utf-8').strip() if i else "" for i in row]
            #row2 = [i.encode('ascii', 'ignore').strip() if i else "" for i in row]
            #row2 = [i.encode('utf-8').strip().decode('utf-8') if i else "" for i in row]
            #row2 = [i.encode('latin-1', 'ignore').strip() if i else "" for i in row]
            #print("Writing :", row2)
            
            writer.writerow(row2)
        mlog("Wrote {} rows to {}".format(line,fname))
        

def dict_parameters(el_list):
    """Given a list of Autodesk.Revit.DB.FamilyInstance. Iterate over each. Collect all paramaters for each. """
    #logging.debug(util_gen.get_self())
    print("*** Processing {} elements".format(len(el_list)))
    total_count = len(el_list)
    dict_list = list()
    for i,el in enumerate(el_list):
        
        #print("{:>10} of {:>10}".format(i+1,total_count))
        
        param_dict = get_all_params(el)
        #print(param_dict)
        dict_list.append(param_dict)
        #for param in el.Parameters: 
        #    print('P')
        
        
    final = {k:[d.get(k) for d in dict_list] for k in {k for d in dict_list for k in d}}
    print("*** Finished processing {} elements".format(len(el_list)))
    return final
    #print(final)
    #for k in final:
    #    print(final[k])



def get_all_params(el):
    this_dict = dict()
    for param in el.Parameters:
        if param.Definition.ParameterType==rvt_db.ParameterType.Text:
            this_dict[param.Definition.Name] = param.AsString()
        else: 
            this_dict[param.Definition.Name] = param.AsValueString()
    return this_dict



def get_all_FamilyInstance(doc):
    """
    Returns FamilyInstance objects only.
    """
    #logging.info("{}".format(util.get_self()))
    
    this_filter = rvt_db.LogicalOrFilter(
      rvt_db.ElementIsElementTypeFilter( False ), 
      rvt_db.ElementIsElementTypeFilter( True ) 
      )
    
    elements = rvt_db.FilteredElementCollector(doc).WherePasses( this_filter).OfClass(rvt_db.FamilyInstance).ToElements()
    
    mlog("Returning {} elements".format(len(elements)))
    
    return elements


def get_sort_all_FamilyInstance(doc):
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
        
    mlog("Returned element dictionary with {} categories of {} in time: {}s".format(len(element_dict), len(elements),end - start))
    
    return element_dict


if __name__ == "__main__":
    run()

