# -*- coding: utf-8 -*-
import copy
import util_geographic
#import pykml
import utm
import simplekml

import csv
import logging
logging.basicConfig(level=logging.DEBUG)
from polycircles import polycircles

#pip install polycircles
#pip install simplekml

# More icons: https://mapicons.mapsmarker.com/

def get_data_csv(path_csv, this_delimiter=';'):
    table_dict = list()
    with open(path_csv) as csvfile:
        
        # First, open the file to get the header, skip one line
        reader = csv.reader(csvfile,delimiter=this_delimiter)
#        skip_row = next(reader)
        headers = next(reader)
        #print(headers)
        #print(type(headers))
        #raise
        # Use the header, re-read, and skip 2 lines
        reader = csv.DictReader(csvfile,fieldnames=headers,delimiter=';')
#        skip_row = next(reader)
#        skip_row = next(reader)
        
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
    logging.debug("Loaded {} sheet definitions with {} columns".format(len(table_dict), len(table_dict[0])))
        
    return table_dict


import sys
logging.info("Python version : {}".format(sys.version))
from decimal import Decimal

path_csv = r"C:\CesCloud Senegal PV\03 Working\Liste des villages\UE List_Finale r03.csv"
data = get_data_csv(path_csv, this_delimiter=';')

path_kml = r"C:\TESTKML"

kml = simplekml.Kml()

def get_scale(pop):
    if pop > 2000:
        pop = 2000
    min_size = 0.8
    max_scale = 1.2
    rise = max_scale/min_size
    run = 3500
    
    slope = rise/run
    
    y_intercept = min_size
    
    this_scale = y_intercept + slope*pop
    
    return this_scale

def get_style(pop):
    if pop < 100:
        return style_dict[100]    
    elif pop < 200:
        return style_dict[200] 
    elif pop < 300:
        return style_dict[300] 
    elif pop < 400:
        return style_dict[400] 
    elif pop < 500:
        return style_dict[500] 
    elif pop < 600:
        return style_dict[600] 
    elif pop < 700:
        return style_dict[700]     
    elif pop < 800:
        return style_dict[800]     
    elif pop < 900:
        return style_dict[900]     
    elif pop < 1500:
        return style_dict[1000]     
    elif pop < 2000:
        return style_dict[2000]
    elif pop >= 2000:
        return style_dict[3000]

    

def convert_coords(x_coord, y_coord):
    pass


    
style_dict = {}
style_dict[100] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/1.png',
                    } 
style_dict[200] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/2.png',
                    } 
style_dict[300] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/3.png',
                    } 
style_dict[400] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/4.png',
                    } 
style_dict[500] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/5.png',
                    } 
style_dict[600] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/6.png',
                    } 
style_dict[700] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/7.png',
                    } 
style_dict[800] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/8.png',
                    } 

style_dict[900] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/9.png',
                    } 
style_dict[1000] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/10.png',
                    } 
style_dict[2000] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/L.png',
                    } 
style_dict[3000] = {"pnt_color" : 'ffff5c82' ,
                    "pnt_icon" : 'http://maps.google.com/mapfiles/kml/paddle/L.png',
                    } 

cnt_cluster = 0
cnt_total = 0
for row in data:
    print("Row:",cnt_total)
    
    # Get coordinates
    try:
        easting = int(row['X_COORD'])
        northing = int(row['Y_COORD'])
    except:
        raise
    lat,lon = utm.to_latlon(easting,northing,28,'P')

    # Get data
    village = row['VILLAGE']
    pop = int(row["POPULATION_ACTUELLE"])
    cluster = row['CLUSTER']

    # Get style
    this_style_dict = copy.deepcopy(get_style(pop))
    
    # Add the scale
    this_style_dict["scale"] = get_scale(pop)
    
    # Overwrite the icon for clustered villages
    if cluster:
        #this_style_dict["pnt_icon"] = "http://maps.google.com/mapfiles/kml/paddle/wht-circle.png"
        this_style_dict["pnt_icon"] = "http://maps.google.com/mapfiles/kml/paddle/wht-blank.png"        
        cnt_cluster += 1
    else:
        pass
    
    # If cluster virtual village:
    if "CLUSTER" in village:
        this_style_dict["pnt_icon"] = "http://maps.google.com/mapfiles/kml/paddle/wht-stars.png"
        this_style_dict["pnt_color"] = "ff00ff00"        
        
    
    # Print definition
    print("{} pop {}  at lat {} long {}, cluster = {}".format(village,pop,lat,lon, cluster))
    print(this_style_dict["pnt_icon"])
    # Write KML
    pnt = kml.newpoint(name=village, coords=[(lon,lat)])
    pnt.description = "{}, population {}".format(village,pop)
    pnt.style.iconstyle.icon.href = this_style_dict["pnt_icon"]
    pnt.style.iconstyle.scale = this_style_dict["scale"]
    
    # Update name of point
    pnt.name = None
    pnt.name = "{}".format(village) #village    
    #pnt.name = "{}".format(pop) #village
    pnt.style.labelstyle.scale = 0.5

print("Cluster villages:", cnt_cluster)

#===============================================================================
# Cluster circles
#===============================================================================
def circles(kml, coords, num, m):
    # 1km     
    polycircle = polycircles.Polycircle(latitude= coords[0],
                                        longitude=coords[1],
                                        radius=m,
                                        number_of_vertices=36)

    pol = kml.newpolygon(name="CLUSTER {} - {} m".format(num,m),outerboundaryis=polycircle.to_kml())
    pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.green)
    pol.style.polystyle.fill = 0

# Cluster 1
circles(kml, (14.786195, -12.564593), 1, 1000 )
circles(kml, (14.786195, -12.564593), 1, 2000 )

# Cluster 2
circles(kml, (14.720557,-12.526910), 2, 1000 )
circles(kml, (14.720557,-12.526910), 2, 2000 )

# Cluster 3
circles(kml, (14.3427075, -12.364911), 3, 1000 )
circles(kml, (14.3427075, -12.364911), 3, 2000 )

# Cluster 4
circles(kml, ( 13.298264, -12.398172), 4, 1000 )
circles(kml, ( 13.298264, -12.398172), 4, 2000 )

# Cluster 5
circles(kml, (14.164446, -13.039861), 5, 1000 )
circles(kml, (14.164446, -13.039861), 5, 2000 )

# Cluster 6
circles(kml, (14.085258, -13.536890), 6, 1000 )
circles(kml, (14.085258, -13.536890), 6, 2000 )

# Cluster 
circles(kml, (14.501643, -13.482537), 7, 1000 )
circles(kml, (14.501643, -13.482537), 7, 2000 )

# Cluster 
circles(kml, (14.622996, -14.627865), 8, 1000 )
circles(kml, (14.622996, -14.627865), 8, 2000 )
 
# Cluster 
circles(kml, (14.658005, -14.686155), 9, 1000 )
circles(kml, (14.658005, -14.686155), 9, 2000 )
    
# Cluster 
circles(kml, ( 14.732937,  -14.776059), 10, 1000 )
circles(kml, ( 14.732937,  -14.776059), 10, 2000 )

# Cluster 11
circles(kml, ( 14.689686,  -14.643279), 11, 1000 )
circles(kml, ( 14.689686,  -14.643279), 11, 2000 )

# Cluster 12
circles(kml, ( 14.9200046,  -14.568823), 12, 1000 )
circles(kml, ( 14.9200046,  -14.568823), 12, 2000 )

# Cluster 13
circles(kml, (15.039622, -14.506272), 13, 1000 )
circles(kml, (15.039622, -14.506272), 13, 2000 )
          

#save_path = path_kml + "\\" +  village + ".kml"
save_path = path_kml + "\\Villages4.kml"
print(save_path)
kml.save(save_path)




