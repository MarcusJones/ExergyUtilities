"""Various utilities used in other modules"""
from __future__ import print_function

#===============================================================================
# Import Revit API
#===============================================================================
try: # For Sphinx
    import Autodesk.Revit.DB as rvt_db
    from Autodesk.Revit.DB import BuiltInCategory

    #from Autodesk.Revit.DB import FilteredElementCollector, 
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
def get_data_csv(path_csv, this_delimiter=';'):
    """Import csv file in a very specific format
    Line 1: SKIP
    Line 2: Headers
    Line 3: (Data starts)
    """
    
    table_dict = list()
    with open(path_csv) as csvfile:
        
        # First, open the file to get the header, skip one line
        reader = csv.reader(csvfile,delimiter=this_delimiter)
        skip_row = next(reader)
        headers = next(reader)
        #print(headers)
        #print(type(headers))
        #raise
        # Use the header, re-read, and skip 2 lines
        reader = csv.DictReader(csvfile,fieldnames=headers,delimiter=';')
        skip_row = next(reader)
        skip_row = next(reader)
        
        for row in reader:
            #print("ROW START")
            op_A = False
            for k in row:
                found = op_A or bool(row[k]) 
                if found: 
                    break
            if not found:
                break
            #print(row)
            table_dict.append(row)
                #if bool(row[k]):
                    
                #    break
                #print(row[k], bool(row[k]))
            
            
            #print(row)
    #print(reader[3])
    logging.debug("Loaded {} rows with {} columns".format(len(table_dict), len(table_dict[0])))
    
    return table_dict

def format_as_table(data,
                    keys,
                    header=None,
                    sort_by_key=None,
                    sort_order_reverse=False):
    """Takes a list of dictionaries, formats the data, and returns
    the formatted data as a text table.
    Required Parameters:
    Args:
    
    data : Data to process (list of dictionaries). (Type: List)
    keys : List of keys in the dictionary. (Type: List)
        
    Optional Parameters:
    header - The table header. (Type: List)
    sort_by_key - The key to sort by. (Type: String)
    sort_order_reverse - Default sort order is ascending, if
    True sort order will change to descending. (Type: Boolean)
    """
    
    # Sort the data if a sort key is specified (default sort order
    # is ascending)
    if sort_by_key:
        data = sorted(data,
                      key=itemgetter(sort_by_key),
                      reverse=sort_order_reverse)

    # If header is not empty, add header to data
    if header:
        # Get the length of each header and create a divider based
        # on that length
        header_divider = []
        for name in header:
            header_divider.append('-' * len(name))

        # Create a list of dictionary from the keys and the header and
        # insert it at the beginning of the list. Do the same for the
        # divider and insert below the header.
        header_divider = dict(zip(keys, header_divider))
        data.insert(0, header_divider)
        header = dict(zip(keys, header))
        data.insert(0, header)

    column_widths = []
    for key in keys:
        column_widths.append(max(len(str(column[key])) for column in data))

    # Create a tuple pair of key and the associated column width for it
    key_width_pair = zip(keys, column_widths)

    format = ('%-*s ' * len(keys)).strip() + '\n'
    formatted_data = ''
    for element in data:
        data_to_format = []
        # Create a tuple that will be used for the formatting in
        # width, value format
        for pair in key_width_pair:
            data_to_format.append(pair[1])
            data_to_format.append(element[pair[0]])
        formatted_data += format % tuple(data_to_format)
    return formatted_data

def get_self():
    """Wrapper for returning string of calling object, for logging.
    """
    return inspect.stack()[1][3]

def print_dir(item):
    """Wrapper for dir()
    """
    for member in dir(item):
        print(member)

class Trans():
    """Context manager for Revit API transactions. 
    """
    def __init__(self, doc, msg):
        self.msg = msg
        self.t = rvt_db.Transaction(doc, msg)
        
    def __enter__(self):
        logging.debug("TRANSACTION INITATIATED - {}".format(self.msg))
        self.t.Start()
    
    def __exit__(self, exception_type, exception_value, traceback):
        logging.debug("TRANSACTION COMPLETE - {}".format(self.msg))
        self.t.Commit()

class ErrorProneTrans():
    """Context manager for Revit API transactions. 
    """
    def __init__(self, doc, msg):
        
        self.msg = msg
        try:
            self.t = rvt_db.Transaction(doc, msg)
        except: 
            print("*** Skipped transaction due to error: {}".format(msg))
        
    def __enter__(self):
        logging.debug("TRANSACTION INITATIATED - {}".format(self.msg))
        self.t.Start()
    
    def __exit__(self, exception_type, exception_value, traceback):
        logging.debug("TRANSACTION COMPLETE - {}".format(self.msg))
        self.t.Commit()


def print_family(fam):
    #print(str(type(fam)))
    #print(str(rvt_db.FamilySymbol))
    #print(str(type(fam)) == str(rvt_db.FamilySymbol))
    
    
    
    if type(fam) == rvt_db.FamilySymbol:
        fam_name = fam.FamilyName
        parent = fam.Family
    elif type(fam) == rvt_db.FamilyInstance:
        fam_name = fam.Name
        parent = fam.Symbol
    else:
        #print("Want", rvt_db.FamilySymbol)
        #print("Got", type(fam))
        #print()
        raise

    #print("Type: {}".format(type(fam)))
    print("{} - {}".format(fam.Category.Name,fam_name))    
    #print("Name: {}".format(str(fam_name)))
    
    

    #print("Parent: {}".format(str(parent)))
    

#-Static globals---
try: # For Sphinx
    REVIT_CATEGORIES_BIC = [
    BuiltInCategory.OST_DuctTerminal                             ,
    #BuiltInCategory.OST_BeamAnalytical                          ,
    #BuiltInCategory.OST_BraceAnalytical                         ,
    #BuiltInCategory.OST_ColumnAnalytical                        ,
    #BuiltInCategory.OST_FloorAnalytical                         ,
    #BuiltInCategory.OST_FoundationSlabAnalytical                ,
    #BuiltInCategory.OST_IsolatedFoundationAnalytical            ,
    #BuiltInCategory.OST_AnalyticalNodes                         ,
    #BuiltInCategory.OST_WallFoundationAnalytical                ,
    #BuiltInCategory.OST_WallAnalytical                          ,
    #BuiltInCategory.OST_AreaLoads                               ,
    #BuiltInCategory.OST_AreaSchemes                             ,
    #BuiltInCategory.OST_Areas                                   ,
    #BuiltInCategory.OST_Assemblies                              ,
    BuiltInCategory.OST_CableTrayFitting                         ,
    BuiltInCategory.OST_CableTrayRun                             ,
    BuiltInCategory.OST_CableTray                                ,
    #BuiltInCategory.OST_Casework                                ,
    #BuiltInCategory.OST_Ceilings                                ,
    #BuiltInCategory.OST_Columns                                 ,
    BuiltInCategory.OST_CommunicationDevices                     ,
    BuiltInCategory.OST_ConduitFitting                           ,
    BuiltInCategory.OST_ConduitRun                               ,
    BuiltInCategory.OST_Conduit                                  ,
    #BuiltInCategory.OST_CurtainWallPanels                       ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_CurtaSystem                             ,
    #BuiltInCategory.OST_CurtainWallMullions                     ,
    BuiltInCategory.OST_DataDevices                              ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_DetailComponents                        ,
    #BuiltInCategory.OST_FilledRegion                            ,
    #BuiltInCategory.OST_MaskingRegion                           ,
    #BuiltInCategory.OST_Doors                                   ,
    BuiltInCategory.OST_DuctAccessory                            ,
    BuiltInCategory.OST_DuctFitting                              ,
    BuiltInCategory.OST_DuctInsulations                          ,
    BuiltInCategory.OST_DuctLinings                              ,
    #BuiltInCategory.OST_PlaceHolderDucts                        ,
    BuiltInCategory.OST_DuctSystem                               ,
    BuiltInCategory.OST_DuctCurves                               ,
    BuiltInCategory.OST_ElectricalCircuit                        ,
    BuiltInCategory.OST_ElectricalEquipment                      ,
    BuiltInCategory.OST_ElectricalFixtures                       ,
    #BuiltInCategory.OST_Entourage                               ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_FabricationParts                        ,
    #BuiltInCategory.OST_Fascia                                  ,
    BuiltInCategory.OST_FireAlarmDevices                         ,
    BuiltInCategory.OST_FlexDuctCurves                           ,
    BuiltInCategory.OST_FlexPipeCurves                           ,
    #BuiltInCategory.OST_Floors                                  ,
    #BuiltInCategory.OST_Furniture                               ,
    #BuiltInCategory.OST_FurnitureSystems                        ,
    #BuiltInCategory.OST_GenericAnnotation                       ,
    #BuiltInCategory.OST_GenericModel                            ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_Grids                                   ,
    #BuiltInCategory.OST_Gutter                                  ,
    #BuiltInCategory.OST_HVAC_Zones                              ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_ImportObjectStyles                      ,
    #BuiltInCategory.OST_InternalAreaLoads                       ,
    #BuiltInCategory.OST_InternalLineLoads                       ,
    #BuiltInCategory.OST_InternalPointLoads                      ,
    #BuiltInCategory.OST_Levels                                  ,
    #BuiltInCategory.                                            ,
    BuiltInCategory.OST_LightingDevices                          ,
    BuiltInCategory.OST_LightingFixtures                         ,
    #BuiltInCategory.OST_Lines                                   ,
    #BuiltInCategory.OST_Lines                                   ,
    #BuiltInCategory.OST_LineLoads                               ,
    #BuiltInCategory.OST_MassFloor                               ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_Mass                                    ,
    #BuiltInCategory.OST_Materials                               ,
    BuiltInCategory.OST_MechanicalEquipment                      ,
    #BuiltInCategory.OST_ModelText                               ,
    BuiltInCategory.OST_NurseCallDevices                         ,
    #BuiltInCategory.OST_BuildingPad                             ,
    #BuiltInCategory.OST_Parking                                 ,
    #BuiltInCategory.OST_Parts                                   ,
    BuiltInCategory.OST_PipeAccessory                            ,
    BuiltInCategory.OST_PipeFitting                              ,
    BuiltInCategory.OST_PipeInsulations                          ,
    BuiltInCategory.OST_PlaceHolderPipes                         ,
    BuiltInCategory.OST_PipeCurves                               ,
    BuiltInCategory.OST_PipingSystem                             ,
    #BuiltInCategory.OST_Planting                                ,
    BuiltInCategory.OST_PlumbingFixtures                         ,
    #BuiltInCategory.OST_PointClouds                             ,
    #BuiltInCategory.OST_PointLoads                              ,
    #BuiltInCategory.OST_ProjectInformation                      ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_SitePropertyLineSegment                 ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_StairsRailing                           ,
    #BuiltInCategory.OST_RailingSupport                          ,
    #BuiltInCategory.OST_RailingTermination                      ,
    #BuiltInCategory.OST_Ramps                                   ,
    #BuiltInCategory.OST_RasterImages                            ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_RevisionClouds                          ,
    #BuiltInCategory.OST_Revisions                               ,
    #BuiltInCategory.OST_Roads                                   ,
    #BuiltInCategory.OST_Roofs                                   ,
    #BuiltInCategory.OST_RoofSoffit                              ,
    #BuiltInCategory.OST_Rooms                                   ,
    #BuiltInCategory.OST_RvtLinks                                ,
    #BuiltInCategory.OST_SecurityDevices                         ,
    #BuiltInCategory.OST_ShaftOpening                            ,
    #BuiltInCategory.OST_Sheets                                  ,
    #BuiltInCategory.OST_Site                                    ,
    #BuiltInCategory.OST_EdgeSlab                                ,
    #BuiltInCategory.OST_MEPSpaces                               ,
    BuiltInCategory.OST_SpecialityEquipment                      ,
    BuiltInCategory.OST_Sprinklers                               ,
    #BuiltInCategory.OST_Stairs                                  ,
    #BuiltInCategory.OST_Stairs                                  ,
    #BuiltInCategory.OST_StairsRuns                              ,
    #BuiltInCategory.OST_StairsSupports                          ,
    #BuiltInCategory.OST_StairsLandings                          ,
    #BuiltInCategory.OST_AreaRein                                ,
    #BuiltInCategory.OST_StructuralFramingSystem                 ,
    #BuiltInCategory.OST_StructuralColumns                       ,
    #BuiltInCategory.OST_StructuralConnectionHandler             ,
    #BuiltInCategory.OST_StructConnections                       ,
    #BuiltInCategory.OST_FabricAreas                             ,
    #BuiltInCategory.OST_FabricReinforcement                     ,
    #BuiltInCategory.OST_StructuralFoundation                    ,
    #BuiltInCategory.OST_StructuralFraming                       ,
    #BuiltInCategory.OST_PathRein                                ,
    #BuiltInCategory.OST_Rebar                                   ,
    #BuiltInCategory.OST_StructuralStiffener                     ,
    #BuiltInCategory.OST_StructuralTruss                         ,
    #BuiltInCategory.                                            ,
    BuiltInCategory.OST_SwitchSystem                             ,
    BuiltInCategory.OST_TelephoneDevices                         ,
    #BuiltInCategory.OST_Topography                              ,
    #BuiltInCategory.OST_Cornices                                ,
    #BuiltInCategory.OST_Walls                                   ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.                                            ,
    #BuiltInCategory.OST_Windows                                 ,
    BuiltInCategory.OST_Wire                                     ,
    ]
except:
    pass



REVIT_CATEGORIES_TEXT = [
# 'Zone Tags',
# 'Wire Tags',
# 'Window Tags',
# 'Wall Tags',
# 'Telephone Device Tags',
# 'Structural Truss Tags',
# 'Structural Stiffener Tags',
# 'Structural Rebar Tags',
# 'Structural Path Reinforcement Tags',
# 'Structural Framing Tags',
# 'Structural Foundation Tags',
# 'Structural Fabric Reinforcement Tags',
# 'Structural Connection Tags',
# 'Structural Column Tags',
# 'Structural Beam System Tags',
# 'Structural Area Reinforcement Tags',
# 'Stair Tags',
# 'Stair Support Tags',
# 'Stair Run Tags',
# 'Stair Landing Tags',
# 'Sprinkler Tags',
# 'Specialty Equipment Tags',
# 'Space Tags',
# 'Site Tags',
# 'Security Device Tags',
# 'Room Tags',
# 'Roof Tags',
# 'Revision Cloud Tags',
# 'Railing Tags',
# 'Property Tags',
# 'Property Line Segment Tags',
# 'Point Load Tags',
# 'Plumbing Fixture Tags',
# 'Planting Tags',
# 'Pipe Tags',
# 'Pipe Insulation Tags',
# 'Pipe Fitting Tags',
# 'Pipe Accessory Tags',
# 'Part Tags',
# 'Parking Tags',
# 'Nurse Call Device Tags',
# 'Multi-Category Tags',
# 'Mechanical Equipment Tags',
# 'Material Tags',
# 'Mass Tags',
# 'Mass Floor Tags',
# 'Line Load Tags',
# 'Lighting Fixture Tags',
# 'Lighting Device Tags',
# 'Keynote Tags',
# 'Internal Point Load Tags',
# 'Internal Line Load Tags',
# 'Internal Area Load Tags',
# 'Generic Model Tags',
# 'Furniture Tags',
# 'Furniture System Tags',
# 'Floor Tags',
# 'Flex Pipe Tags',
# 'Flex Duct Tags',
# 'Fire Alarm Device Tags',
# 'Fabrication Part Tags',
# 'Electrical Fixture Tags',
# 'Electrical Equipment Tags',
# 'Duct Tags',
# 'Duct Lining Tags',
# 'Duct Insulation Tags',
# 'Duct Fitting Tags',
# 'Duct Accessory Tags',
# 'Door Tags',
# 'Detail Item Tags',
# 'Data Device Tags',
# 'Curtain System Tags',
# 'Curtain Panel Tags',
# 'Conduit Tags',
# 'Conduit Fitting Tags',
# 'Communication Device Tags',
# 'Ceiling Tags',
# 'Casework Tags',
# 'Cable Tray Tags',
# 'Cable Tray Fitting Tags',
# 'Assembly Tags',
# 'Area Tags',
# 'Area Load Tags',
# 'Analytical Wall Tags',
# 'Analytical Wall Foundation Tags',
# 'Analytical Slab Foundation Tags',
# 'Analytical Node Tags',
# 'Analytical Link Tags',
# 'Analytical Isolated Foundation Tags',
# 'Analytical Floor Tags',
# 'Analytical Column Tags',
# 'Analytical Brace Tags',
# 'Analytical Beam Tags',
# 'Air Terminal Tags',
 'Wires',
# 'Windows',
# 'Walls',
# 'Views',
# 'Viewports',
# 'View Titles',
# 'View Reference',
# 'Topography',
# 'Title Blocks',
# 'Text Notes',
 'Telephone Devices',
 'Switch System',
# 'Structural Trusses',
# 'Structural Stiffeners',
# 'Structural Rebar',
# 'Structural Path Reinforcement Symbols',
# 'Structural Path Reinforcement',
# 'Structural Loads',
# 'Structural Load Cases',
# 'Structural Internal Loads',
# 'Structural Framing',
# 'Structural Foundations',
# 'Structural Fabric Reinforcement Symbols',
# 'Structural Fabric Reinforcement',
# 'Structural Fabric Areas',
# 'Structural Connections',
# 'Structural Connection Handlers',
# 'Structural Columns',
# 'Structural Beam Systems',
# 'Structural Area Reinforcement Symbols',
# 'Structural Area Reinforcement',
# 'Structural Annotations',
# 'Stairs',
# 'Stair Tread/Riser Numbers',
# 'Stair Paths',
 'Sprinklers',
# 'Spot Slopes',
# 'Spot Elevations',
# 'Spot Elevation Symbols',
# 'Spot Coordinates',
 'Specialty Equipment',
# 'Span Direction Symbol',
# 'Spaces',
# 'Site',
# 'Sheets',
# 'Shaft Openings',
 'Security Devices',
# 'Sections',
# 'Section Marks',
# 'Section Line',
# 'Section Boxes',
# 'Scope Boxes',
# 'Schedule Graphics',
# 'Routing Preferences',
# 'Rooms',
# 'Roofs',
# 'Roads',
# 'Revision Clouds',
# 'Render Regions',
# 'Reference Points',
# 'Reference Planes',
# 'Reference Lines',
# 'Rebar Shape',
# 'Rebar Set Toggle',
# 'Rebar Cover References',
# 'Raster Images',
# 'Ramps',
# 'Railings',
# 'Project Information',
# 'Point Clouds',
 'Plumbing Fixtures',
# 'Planting',
# 'Plan Region',
 'Piping Systems',
 'Pipes',
 'Pipe Segments',
 'Pipe Placeholders',
 'Pipe Insulations',
 'Pipe Fittings',
# 'Pipe Color Fill Legends',
# 'Pipe Color Fill',
 'Pipe Accessories',
 'Parts',
# 'Parking',
# 'Panel Schedule Graphics',
 'Nurse Call Devices',
# 'Multi-Rebar Annotations',
 'Mechanical Equipment',
# 'Materials',
# 'Matchline',
# 'Mass',
# 'Masking Region',
# 'Lines',
 'Lighting Fixtures',
 'Lighting Devices',
# 'Levels',
# 'Level Heads',
# 'Imports in Families',
# 'HVAC Zones',
# 'Guide Grid',
# 'Grids',
# 'Grid Heads',
 'Generic Models',
# 'Generic Annotations',
# 'Furniture Systems',
# 'Furniture',
# 'Foundation Span Direction Symbol',
# 'Floors',
 'Flex Pipes',
 'Flex Ducts',
 'Fire Alarm Devices',
# 'Filled region',
 'Fabrication Parts',
# 'Entourage',
# 'Elevations',
# 'Elevation Marks',
 'Electrical Fixtures',
 'Electrical Equipment',
 'Ducts',
 'Duct Systems',
 'Duct Placeholders',
 'Duct Linings',
 'Duct Insulations',
 'Duct Fittings',
# 'Duct Color Fill Legends',
# 'Duct Color Fill',
 'Duct Accessories',
# 'Doors',
# 'Displacement Path',
# 'Dimensions',
# 'Detail Items',
 'Data Devices',
# 'Curtain Wall Mullions',
# 'Curtain Systems',
# 'Curtain Panels',
# 'Curtain Grids',
# 'Contour Labels',
# 'Connection Symbols',
 'Conduits',
 'Conduit Runs',
 'Conduit Fittings',
 'Communication Devices',
# 'Columns',
# 'Color Fill Legends',
# 'Ceilings',
# 'Casework',
# 'Cameras',
# 'Callouts',
# 'Callout Heads',
# 'Callout Boundary',
 'Cable Trays',
 'Cable Tray Runs',
 'Cable Tray Fittings',
# 'Brace in Plan View Symbols',
# 'Boundary Conditions',
 'Assemblies',
# 'Areas',
# 'Analytical Walls',
# 'Analytical Wall Foundations',
# 'Analytical Surfaces',
# 'Analytical Spaces',
# 'Analytical Nodes',
# 'Analytical Links',
# 'Analytical Isolated Foundations',
# 'Analytical Foundation Slabs',
# 'Analytical Floors',
# 'Analytical Columns',
# 'Analytical Braces',
# 'Analytical Beams',
# 'Analysis Results',
# 'Analysis Display Style',
 'Air Terminals',
# 'Adaptive Points',
                  ]

