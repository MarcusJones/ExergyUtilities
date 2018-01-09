"""For manipulation of geometric objects in Revit"""
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

#-Geometry---
def apply_crop(doc,view, bound_box):
    logging.debug("apply_crop")
    
    # Adjust Crop on existing
    crop_manager = view.GetCropRegionShapeManager()
    logging.debug("Crop manager valid {}".format(crop_manager.Valid))
    
    #if 0 :
        #assert crop_manager.Valid, "Crop manager invalid"

    with util.Trans(doc, "Adjust crop"):
        #crop_manager.SetCropRegionShape(bound_box)
        crop_manager.SetCropShape(bound_box)
        logging.debug("Cropped {}".format(view))

def get_bound_box(grid_bounds, oversize_factor):
    logging.debug("get_grids")
    
    # Given a dict of l,r,t,b to grid elements
    # Return a bonding box CurveLoop object
    # With rectangle increased oversize_factor
    
    # Get the X and Y unscaled bounds
    left_x = grid_bounds['left'].Curve.GetEndPoint(0).X
    right_x = grid_bounds['right'].Curve.GetEndPoint(0).X
    bot_y = grid_bounds['bot'].Curve.GetEndPoint(0).Y
    top_y = grid_bounds['top'].Curve.GetEndPoint(0).Y
    
    # Temporarily create box lines, to get scale factor
    top_line = Line.CreateBound(XYZ(left_x, top_y, 0), XYZ(right_x, top_y, 0))
    right_line = Line.CreateBound(XYZ(right_x, top_y, 0), XYZ(right_x, bot_y, 0))
    bot_line = Line.CreateBound(XYZ(right_x, bot_y, 0), XYZ(left_x, bot_y, 0))
    left_line = Line.CreateBound(XYZ(left_x, bot_y, 0), XYZ(left_x, top_y, 0))
    
    # Calculate scale adjustments
    X_scale = top_line.Length*oversize_factor
    Y_scale = right_line.Length*oversize_factor
    
    # Apply the scaling
    left_x = grid_bounds['left'].Curve.GetEndPoint(0).X - X_scale
    right_x = grid_bounds['right'].Curve.GetEndPoint(0).X + X_scale
    bot_y = grid_bounds['bot'].Curve.GetEndPoint(0).Y - Y_scale
    top_y = grid_bounds['top'].Curve.GetEndPoint(0).Y + Y_scale

    # Create the scaled box lines
    top_line = Line.CreateBound(XYZ(left_x, top_y, 0), XYZ(right_x, top_y, 0))
    right_line = Line.CreateBound(XYZ(right_x, top_y, 0), XYZ(right_x, bot_y, 0))
    bot_line = Line.CreateBound(XYZ(right_x, bot_y, 0), XYZ(left_x, bot_y, 0))
    left_line = Line.CreateBound(XYZ(left_x, bot_y, 0), XYZ(left_x, top_y, 0))
        
    # Create a loop object
    bound_box = CurveLoop()    
    # Need to APPEND the lines
    bound_box.Append(top_line)
    bound_box.Append(right_line)
    bound_box.Append(bot_line)
    bound_box.Append(left_line)    
    
    assert not bound_box.IsOpen(), "Box not closed"
    
    print("Created curve element box".format(grid_bounds))

    return bound_box



def get_uv_center(this_sheet):

    #print(this_sheet.Outline)
    #print()
    #print()
    
    center_u = (this_sheet.Outline.Max[0] - this_sheet.Outline.Min[0])/2 + this_sheet.Outline.Min[0]
    center_v = (this_sheet.Outline.Max[1] - this_sheet.Outline.Min[1])/2 + this_sheet.Outline.Min[1]
    centerUV = rvt_db.UV(center_u,center_v) 
    
    logging.debug("Box {} {} with center point {}".format(this_sheet.Outline.Min, this_sheet.Outline.Max, centerUV))
    return centerUV
