
# -*- coding: utf-8 -*-
import copy
import csv
import logging
import os
import utility_excel_api as util_xl
from collections import defaultdict
from tables.hdf5extension import VLArray
#from ExergyUtilities.senegal_process_excel import get_village_row_dict
logging.basicConfig(level=logging.DEBUG)


#https://msdn.microsoft.com/en-us/library/office/jj231257.aspx
#http://www.jkp-ads.com/Articles/Excel2007TablesVBA.asp

path_dir = r"C:\CesCloud Senegal PV\03 Working\Liste des villages"
name_file = r"UE List_Finale r21.xlsx"

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

def group_clusters(table_villages):
    col_headers = get_column_index_dict(table_villages)
    tgt_col = col_headers["CLUSTER_NUMBER"]
    
    cluster_rows = defaultdict(list)
    
    for i,row_obj in enumerate(table_villages.ListRows):
        idx_xl = i + 1
        this_row = table_villages.ListRows(idx_xl).Range
        cluster_num = table_villages.ListRows(idx_xl).Range(tgt_col).Value
        if cluster_num:
            cluster_num = int(cluster_num)
            print(cluster_num)
            cluster_rows[cluster_num].append(this_row)

    for k in cluster_rows:
        print(k)
        number_villages = len(cluster_rows[k])
        eastings = list()
        northings = list()        
        logging.info("Processing cluster {} with {} villages".format(k,number_villages))
        
        for row in cluster_rows[k]:
            print(row)
            # Collect 
            tgt_col = col_headers["X_COORD"]
            eastings.append(row(1,tgt_col).Value)
            tgt_col = col_headers["Y_COORD"]
            northings.append(row(1,tgt_col).Value)
        #-0 Calculate center of mass
        #print(eastings)
        avg_easting = sum(eastings)/number_villages
        #print(avg_eastings)
        
        #print(northings)
        avg_northing = sum(northings)/number_villages
        #print(avg_northings)

        

def get_villages(xl):
    pass
    
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
            
        
        group_clusters(table_villages)
        
        #get_column_index_dict(table)


                #print("Cluster {} Village {} on row {}".format(cluster_num,village,village_row_dict[village]))
                
        
        
        #get_village_row(table_villages,"BODE")
        
        
        #xl.save_and_close()
        #for 
        #get_village()
        


if __name__ == "__main__":
    main()
    
        