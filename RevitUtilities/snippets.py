"""This module contains some tools for using the Revit API"""
from __future__ import print_function

#===============================================================================
# Import Revit API
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
# Import Python
#===============================================================================
#import System
import inspect
import csv
#from collections import defaultdict
#import time
import logging
from operator import itemgetter


#-Utility---

"""
static FilteredElementCollector GetConnectorElements(
  Document doc,
  bool include_wires )
{
  // what categories of family instances
  // are we interested in?
 
  BuiltInCategory[] bics = new BuiltInCategory[] {
    //BuiltInCategory.OST_CableTray,
    BuiltInCategory.OST_CableTrayFitting,
    //BuiltInCategory.OST_Conduit,
    BuiltInCategory.OST_ConduitFitting,
    //BuiltInCategory.OST_DuctCurves,
    BuiltInCategory.OST_DuctFitting,
    BuiltInCategory.OST_DuctTerminal,
    BuiltInCategory.OST_ElectricalEquipment,
    BuiltInCategory.OST_ElectricalFixtures,
    BuiltInCategory.OST_LightingDevices,
    BuiltInCategory.OST_LightingFixtures,
    BuiltInCategory.OST_MechanicalEquipment,
    //BuiltInCategory.OST_PipeCurves,
    BuiltInCategory.OST_PipeFitting,
    BuiltInCategory.OST_PlumbingFixtures,
    BuiltInCategory.OST_SpecialityEquipment,
    BuiltInCategory.OST_Sprinklers,
    //BuiltInCategory.OST_Wire,
  };
 
  IList<ElementFilter> a
    = new List<ElementFilter>( bics.Count() );
 
  foreach( BuiltInCategory bic in bics )
  {
    a.Add( new ElementCategoryFilter( bic ) );
  }
 
  LogicalOrFilter categoryFilter
    = new LogicalOrFilter( a );
 
  LogicalAndFilter familyInstanceFilter
    = new LogicalAndFilter( categoryFilter,
      new ElementClassFilter(
        typeof( FamilyInstance ) ) );
 
  IList<ElementFilter> b
    = new List<ElementFilter>( 6 );
 
  b.Add( new ElementClassFilter( typeof( CableTray ) ) );
  b.Add( new ElementClassFilter( typeof( Conduit ) ) );
  b.Add( new ElementClassFilter( typeof( Duct ) ) );
  b.Add( new ElementClassFilter( typeof( Pipe ) ) );
 
  if( include_wires )
  {
    b.Add( new ElementClassFilter( typeof( Wire ) ) );
  }

  b.Add( familyInstanceFilter );
 
  LogicalOrFilter classFilter
    = new LogicalOrFilter( b );
 
  FilteredElementCollector collector
    = new FilteredElementCollector( doc );
 
  collector.WherePasses( classFilter );
 
  return collector;
}
"""

#-OLD---
def check_sheets_exist(table_dict, sheets_by_name):
    count_missing = 0
    count_total = 0
    for row in table_dict:
        if row['SOURCE'] == 'RVT':
#             print("{} {}".format(row['NUMBER ON SHEET'],
#                                   row['NAME ON SHEET']))
#             
            try:
                sheets_by_name[row['Sheet Name']]
                count_total += 1
            except:
                logging.error("Missing sheet:{} {}".format(row['Sheet Number'],row['Sheet Name']))
                count_missing += 1
        if count_missing: 
            raise Exception("{} missing sheets_by_name".format(count_missing))
     
    logging.debug("Checked {} RVT sheets_by_name by sheet name - all names exist.".format(count_total))
