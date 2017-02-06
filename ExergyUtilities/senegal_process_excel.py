
# -*- coding: utf-8 -*-
import copy
import csv
import logging
import os
import utility_excel_api as util_xl
from collections import defaultdict
from tables.hdf5extension import VLArray
from util_pretty_print import print_table
#from ExergyUtilities.senegal_process_excel import get_village_row_dict
logging.basicConfig(level=logging.DEBUG)


#http://www.jkp-ads.com/Articles/Excel2007TablesVBA.asp
#https://msdn.microsoft.com/en-us/library/office/jj231257.aspx

path_dir = r"C:\CesCloud Senegal PV\03 Working\Liste des villages"
name_file = r"UE List_Finale r28.xlsx"

full_path = os.path.join(path_dir,name_file)

def get_clusters_dict(xl):
    """
    Return a dictionary of cluster_number : [village names]
    """
    table_clusters = xl.get_table("Clusters", "tab_Clusters")
    dict_cluster = defaultdict(list)
    for i,row in enumerate(table_clusters.ListRows):
        cluster, village = (table_clusters.ListRows(i+1).Range)
        dict_cluster[int(cluster)].append(village.__str__())
    return dict_cluster

def cluster_num(clusters_dict, village_name):
    pass

def get_column_index_dict(table):
    dict_cols = {}
    for i,item in enumerate(table.ListColumns):
        # ADD ONE FOR EXCEL INDEXING
        dict_cols[item.__str__()] = i+1
        #print(i,item)
    return dict_cols

def get_village_row_dict(table_villages):
    # Which column? 
    col_dict = get_column_index_dict(table_villages)
    name_row_idx = col_dict["VILLAGE"]
    
    village_row_dict = {}
    
    # Which row? 
    for i,row in enumerate(table_villages.ListRows):
        this_name = table_villages.ListRows(i+1).Range(name_row_idx)
        this_name = this_name.__str__()
        # ADD ONE FOR EXCEL INDEXING        
        village_row_dict[this_name] = i + 1
        
    return village_row_dict

def get_village_row(table_villages,village_name):
    # Switched to DICT
    #raise
    # Which column? 
    col_dict = get_column_index_dict(table_villages)
    name_row_idx = col_dict["VILLAGE"]
    #print(name_row_idx)
    
    # Which row? 
    for i,row in enumerate(table_villages.ListRows):
        this_name = table_villages.ListRows(i+1).Range(name_row_idx)
        this_name = this_name.__str__()
        #print(i,this_name)
        
        if this_name == village_name:
            
            logging.debug("Match {} {} {}".format(this_name, village_name,i ))
            return i
        else:
            #print(type(this_name))
            #print(type(village_name)) 
            #logging.debug("NO Match {} {} {}".format(this_name, village_name,i))
            pass
    raise KeyError("{} not in list".format(village_name))
    
    #print(table_villages.Column["VILLAGE"])
    #oSh.Range("Table1[Column2]").Select
    #raise

def number_clusters(dict_clusters,village_row_dict,data_headers,table_villages):
    # Write the cluster number to the appropriate column in Excel for each village
    print(dict_clusters)
    
    for k in dict_clusters:
        cluster_num = k
        villages_in_cluster = dict_clusters[k]
        #print("{} - {}".format(k, ))
        
        # Check data match between clusters and village names
        for village in villages_in_cluster:
            if not village in village_row_dict:
                raise KeyError("{} not in list".format(village))
            
            tgt_row = village_row_dict[village]
            tgt_col = data_headers["CLUSTER_NUMBER"]
            
            table_villages.ListRows(tgt_row).Range(1,tgt_col).Value = cluster_num
            logging.info("Wrote cluster {} to village {} [{},{}]".format(cluster_num,village,tgt_row,tgt_col))

def average_for_coords(coord_list):
    return sum(coord_list)/len(coord_list)

def process_column(rows, tgt_col, new_row, function):
    """
    Update ROW list for the function applied to all source row
    """
    collector_list = list()
    for row in rows:
        #print(row)
        if row(1,tgt_col).Value:
            collector_list.append(row(1,tgt_col).Value)
        
    # Re-index -1 for python
    new_row[tgt_col-1] = function(collector_list)
    return new_row

def group_clusters(table_villages):
    col_headers = get_column_index_dict(table_villages)
    col_headers_list = table_villages.ListColumns
    
    cluster_rows = defaultdict(list)
    
    
    for i,row_obj in enumerate(table_villages.ListRows):
        idx_xl = i + 1
        this_row = table_villages.ListRows(idx_xl).Range
        cluster_num = table_villages.ListRows(idx_xl).Range(col_headers["CLUSTER_NUMBER"]).Value
        if cluster_num:
            cluster_num = int(cluster_num)
            cluster_rows[cluster_num].append(this_row)
    
    for k in cluster_rows:
        #print(k)
        number_villages = len(cluster_rows[k])
        logging.info("Processing cluster {} with {} villages".format(k,number_villages))
        
        village_names = list()
        for row in cluster_rows[k]:
            village_names.append(str(row[col_headers["VILLAGE"] -1 ] ))
            new_row = [None for i in range(len(row))]
        
        new_row[col_headers["CLUSTERED VILLAGES"] -1 ] = ", ".join(village_names)
        
        new_row[col_headers["VILLAGE"] -1 ] = "Cluster {} with {} villages".format(k,number_villages)

        #---Calculate center of mass
        new_row = process_column(cluster_rows[k], col_headers["X_COORD"], new_row, average_for_coords)
        new_row = process_column(cluster_rows[k], col_headers["Y_COORD"], new_row, average_for_coords)

        
        
        # Population
        new_row = process_column(cluster_rows[k], col_headers["POPULATION_ACTUELLE"], new_row, sum)
        
        # Menage
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE MENAGE"], new_row, sum)
        
        # Conncession
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE CONCESSION"], new_row, sum)
        
        # Conncession
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE BOUTIQUE "], new_row, sum)
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE D'ATELIER"], new_row, sum)
       
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE FORAGE/ POMPAGE MANUEL"], new_row, sum)        
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE D'ECOLE"], new_row, sum)
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE CASE DE SANTE"], new_row, sum)
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE MOSQUEE"], new_row, sum)
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE MARCHE"], new_row, sum)
        
        new_row = process_column(cluster_rows[k], col_headers["NOMBRE DE MOULIN"], new_row, sum)
        
        new_row[col_headers["COUNT CLUSTERED"] -1 ] = number_villages
        
        # Apply from previous row
        new_row[col_headers["COMMUNE"]  -1] = row(1,col_headers["COMMUNE"])  
        new_row[col_headers["DEPARTEMENT"] -1 ] = row(1,col_headers["DEPARTEMENT"]) 
        new_row[col_headers["REGION"]  -1 ] = row(1,col_headers["REGION"]) 
        
        print_table([col_headers_list,new_row])
        insert_row = table_villages.ListRows.Add(1)

        for i,item in enumerate(insert_row.Range.Value[0]):
            xl_index = i +1
            
            #print(i,new_row[i])
            insert_row.Range(1,xl_index).Value = new_row[i]
        
def apply_region_numbers(table_villages):
    col_headers = get_column_index_dict(table_villages)
    col_headers_list = table_villages.ListColumns
    selection1 = "MATAM","KANEL","RANEROU FERLO" 
    selection2 = "GOUDIRY","BAKEL"
    #oSh.Range("Table1[Column2]").Select

    for i,row_obj in enumerate(table_villages.ListRows):
        idx_xl = i + 1
        this_row = table_villages.ListRows(idx_xl).Range
        region = table_villages.ListRows(idx_xl).Range(col_headers["DEPARTEMENT"]).Value
        print(region)
        if region in selection1:
            table_villages.ListRows(idx_xl).Range(col_headers["DEPARTEMENT"]).Value
            #table_villages.ListRows(tgt_row).Range(1,tgt_col).Value = cluster_num
            
            print("1")
        elif region in selection2:
            print("2")
        else:
            print(this_row)
            raise
        
    
#     
#     for row in table_villages.Range:
#         print(row)
#     
#         # Check data match between clusters and village names
#         for village in villages_in_cluster:
#             if not village in village_row_dict:
#                 raise KeyError("{} not in list".format(village))
#             
#             tgt_row = village_row_dict[village]
#             tgt_col = data_headers["CLUSTER_NUMBER"]
#             
#             table_villages.ListRows(tgt_row).Range(1,tgt_col).Value = cluster_num
#             logging.info("Wrote cluster {} to village {} [{},{}]".format(cluster_num,village,tgt_row,tgt_col))


        

    
def main():
    print(full_path)
    with util_xl.ExtendedExcelBookAPI(full_path) as xl:
        print(xl)
        
        print(xl.get_sheet_names())
        
        # Get clusters
        dict_clusters = get_clusters_dict(xl)

        # Get villages table
        table_villages = xl.get_table("Villages", "tab_Villages")
        data_headers = get_column_index_dict(table_villages)
        # Get village name : rows
        village_row_dict = get_village_row_dict(table_villages)
        
        if 0:
            number_clusters(dict_clusters,village_row_dict,data_headers,table_villages)
            
        if 0:
            group_clusters(table_villages)
        
        apply_region_numbers(table_villages)
        
        #get_column_index_dict(table)


                #print("Cluster {} Village {} on row {}".format(cluster_num,village,village_row_dict[village]))
                
        
        
        #get_village_row(table_villages,"BODE")
        
        
        #xl.save_and_close()
        #for 
        #get_village()
        


if __name__ == "__main__":
    main()
    
        

#---- OLD
#         
#         #print(eastings)
#         avg_easting = sum(eastings)/number_villages
#         #print(avg_eastings)
#         
#         #print(northings)
#         avg_northing = sum(northings)/number_villages
#         #print(avg_northings)
#         
#         #---Sum population
#         total_pop = sum(population) 
#         print(total_pop)
#         
#         #---Sum menage
#         total_menage = sum(menage)
#         print(total_menage)
#         
#         #---Sum concession
#         #print(conncession)
#         total_conncession = sum(conncession)
#         print(total_conncession)
# 
#             # Collect coordinates 
#             tgt_col = col_headers["X_COORD"]
#             eastings.append(row(1,tgt_col).Value)
#             tgt_col = col_headers["Y_COORD"]
#             northings.append(row(1,tgt_col).Value)
#             
#             # Collect Population
#             tgt_col = col_headers["POPULATION_ACTUELLE"]
#             population.append(row(1,tgt_col).Value)
#             
#             # Collect Menage
#             tgt_col = col_headers["NOMBRE DE MENAGE"]
#             this_menage = row(1,tgt_col).Value
#             menage.append(this_menage)
#             
#             # Collect conncession
#             tgt_col = col_headers["NOMBRE DE CONCESSION"]
#             this_conncession = row(1,tgt_col).Value
#             if this_conncession:
#                 conncession.append(this_conncession)