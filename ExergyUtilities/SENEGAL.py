# -*- coding: utf-8 -*-
import util_geographic
#import pykml

import simplekml
import csv
import logging
logging.basicConfig(level=logging.DEBUG)


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

path_csv = r"C:\CesCloud Senegal PV\03 Working\Selection of villages\160627 UE - Liste des villages (coordonnees) MJ.csv"
data = get_data_csv(path_csv, this_delimiter=';')

path_kml = r"C:\TESTKML"

count_total = 0
count_small = 0
count_medium = 0
count_large = 0

kml = simplekml.Kml()

for row in data:
    if row['Distance réseau SENELEC existant ou réseau projeté '] == '7<d<40':
        #print(row)
        #print(row['Distance réseau SENELEC existant ou réseau projeté '])

        #print("{} {}".format(row['LATITUDE'],row['LONGITUDE']))
        
        row['LATITUDE'] = row['LATITUDE'].replace(',','.')
        row['LONGITUDE'] = row['LONGITUDE'].replace(',','.')
        try:
            lat = Decimal(row['LATITUDE'])
            long = Decimal(row['LONGITUDE'])
        except:
            #print("PROBLEM {}".format(row['LATITUDE']))
            #print(lat)
            #print(long)
            #raise
            pass
            #print(lat)
            #raise
        #print("***************")
        #print("{} {}".format(lat,long))
        #print("{} {}".format(type(lat),type(long)))
        assert(type(lat) == Decimal)
        assert(type(long) == Decimal)
        
        village = row['VILLAGE']
        pop = int(row["Estimation (En utilisant formule d'extrapolation et Information PEPAM)"])
        
        if pop < 400:
            village_size = 'small'
            pnt_scale = 0.9
            pnt_color = 'ffffae9c'
            pnt_icon = 'http://maps.google.com/mapfiles/kml/paddle/S.png'
            #            'ffff0000'
            count_small += 1
            
        elif pop < 600:
            village_size = 'medium'
            pnt_scale = 1
            pnt_color = 'ffff5c82' 
            pnt_icon = 'http://maps.google.com/mapfiles/kml/paddle/M.png'

            
            count_medium += 1
        elif pop < 2000:
            village_size = 'large'
            pnt_scale = 1.2
            count_large += 1
            #pnt_color = 'ffff0000'  
            pnt_color = 'ffff5c82' 
            pnt_icon = 'http://maps.google.com/mapfiles/kml/paddle/L.png'


        else:
            raise 
        
        print("{} pop {} ({}) at lat {} long {}".format(village,pop,village_size,lat,long))
        count_total += 1
        
        
        pnt = kml.newpoint(name=village, coords=[(long,lat)])
        pnt.description = "{}, population {}".format(village,pop)
        
        #pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/info-i.png'
        pnt.style.iconstyle.icon.href = pnt_icon
        #'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png'
        #pnt.style.iconstyle.icon.href = r"http://maps.google.com/mapfiles/kml/shapes/open-diamond.png"
        
        pnt.style.iconstyle.scale = pnt_scale
        #pnt.style.iconstyle.color = pnt_color
        #pnt.style.iconstyle.color =   # Blue
        
        pnt.name = None
        pnt.name = "{}".format(pop)#village
        
        #pnt.style.labelstyle.scale = pnt_scale
        
        
        
        
    else:
        continue

print("Total: " + str(count_total))
print("Small: " + str(count_small))
print("Medium: " + str(count_medium))
print("Large: " + str(count_large))    



#save_path = path_kml + "\\" +  village + ".kml"
save_path = path_kml + "\\Villages2.kml"
print(save_path)
kml.save(save_path)