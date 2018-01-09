from __future__ import print_function
import csv
import logging 
logging.basicConfig(level=logging.DEBUG)


def get_data_csv(path_csv, this_delimiter=';'):
    table_dict = list()
    with open(path_csv) as csvfile:
        
        # First, open the file to get the header, skip one line
        #reader = csv.reader(csvfile,delimiter=this_delimiter)
        #headers = next(reader)
        #print(headers)
        #print(type(headers))
        #raise
        # Use the header, re-read, and skip 2 lines
        #reader = csv.DictReader(csvfile,fieldnames=headers,delimiter=';')
        reader = csv.DictReader(csvfile,delimiter=';')
        
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



#-Paths---
folder_csv = r"C:\CesCloud Revit\_03_IKEA_Working_Folder\BOQ Development"
name_csv = r"\BOQ ALL.csv"
path_csv = folder_csv + name_csv

#-Get data---
table = get_data_csv(path_csv)
compound_key_list = ('Category','Workset','Family','Type','Size','System')
report_cols = ('Description','ifcDescription','Length','Area')
#print(table[0])
#tab = list()
for row in table:
    compount_row = dict()
    # For all rows, create a compound key tuple 
    key_val_tuple = [row[this_key] for this_key in compound_key_list]
    row['compound_key'] = tuple(key_val_tuple)
    
    #for this_key in report_cols:
    #    compound_row
    
    #report_val_tuple = [row[this_key] for this_key in report_cols]
    #compount_row['compound_key'] = key_val_tuple

# Get all unique compound keys

#for row in table[0:10]:
#    print(row['compound_key'])
    
    

compound_keys = list()
for row in table:
    #print(row['compound_key'])
    if not row['compound_key'] in compound_keys:
        compound_keys.append(row['compound_key'])
    #compound_keys.update(row['compound_key'])

logging.debug("{} unique compound keys".format(len(compound_keys)))    


sum_table = list()
for ckey in compound_keys:
    sub_table = list()
    for row in table:
        #print(ckey)
        #print(row['compound_key'])
        #print(ckey==row['compound_key'])
        if ckey == row['compound_key']:
            # Collect all these rows
            sub_table.append(row)
        #print(len(sub_table))
    assert len(sub_table)>0        
    logging.debug("Sub-table {} with {} rows".format(ckey,len(sub_table)))
    #print(sub_table)
    # Build up the new row
    new_row = dict()
    for key in compound_key_list:
        print()
        new_row[key] = sub_table[0][key]
        
        
    new_row['Description'] =  sub_table[0]['Description']
    new_row['ifcDescription'] =  sub_table[0]['ifcDescription']
    sum_length = 0
    sum_area = 0
    for sub_row in sub_table:
        if sub_row['Length'] != 'DNE':
            try:
                sum_length += float(sub_row['Length'])
            except:
                print(sub_row['Length'])
        if sub_row['Area'] != 'DNE':
            #print(repr(sub_row['Area']))
            #raise
            try:
                sum_area += float(sub_row['Area'])
            except:
                print(sub_row['Area'])
                
            
    new_row['Sum Length'] = sum_length
    new_row['Sum Area'] = sum_area
    
    sum_table.append(new_row)

out_path = r"C:\CesCloud Revit\_03_IKEA_Working_Folder\BOQ Development\BOQ Summed.csv"
with open(out_path,'wb') as csv_file:
    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=sum_table[0].keys())
    writer.writeheader()
    writer.writerows(sum_table)

logging.info("Wrote {} rows in  table to {} ".format(len(sum_table),out_path))
