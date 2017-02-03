
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
from time import sleep


#https://msdn.microsoft.com/en-us/library/office/jj231257.aspx
#http://www.jkp-ads.com/Articles/Excel2007TablesVBA.asp

path_dir = r"C:\CesCloud Senegal PV\03 Working\Liste des villages\Fiche Enquete\1"
name_file = r"Fiche_Enquete_Matam_Equipe 1.xlsx"

full_path = os.path.join(path_dir,name_file)
    
def main():
    print(full_path)
#     with util_xl.ExtendedExcelBookAPI(full_path) as xl:
#         print(xl)
#         
#         #print()
#         
#         sheets = xl.get_sheet_names()
#         #for i,sh in enumerate(sheets):
#         #    print(i,sh)
#         
#         sheets = [(i,sh) for i,sh in enumerate(sheets)]
#         
#     print(sheets)
#     for sheet_def in sheets:
#         print(sheet_def)
#         with util_xl.ExtendedExcelBookAPI(full_path) as xl:
#             print(xl)
#             
#             #xl.write_book._Workbook__worksheets = [write_book._Workbook__worksheets[0]]
#             
    with util_xl.ExtendedExcelBookAPI(full_path) as xl:
        print(xl.book)
        xl.DisplayAlerts = False
        for sheet in xl.book.Worksheets:
            print("Processing", sheet.name)
            #raise
            new_workbook = copy.copy(xl.book)
            #new_workbook.DisplayAlerts = False
            #raise
            
            for worksheet in new_workbook.Worksheets:
                if worksheet.name == sheet.name:
                    print("Skipping:",worksheet.name)
                else:
                    sleep(0.05)
                    print("Deleting:",worksheet.name)
                    worksheet.Delete()
                    
                    
            sleep(1)
            #new_workbook.Worksheets = [ worksheet for worksheet in new_workbook.Worksheets if worksheet.name == sheet.name ]
            #print(new_workbook)
            
            new_full_path = os.path.join(path_dir,'{}_split.xls'.format(sheet.name))
            new_workbook.SaveAs(new_full_path)  
            new_workbook.Close(SaveChanges=0) # see note 1

#     # OTHER
#     # Process each sheet
#     for sheet in workbook.sheets():
#         # Make a copy of the master worksheet
#         new_workbook = copy.copy(workbook)
#     
#         # for each time we copy the master workbook, remove all sheets except
#         #  for the curren sheet (as defined by sheet.name)
#         new_workbook._Workbook__worksheets = [ worksheet for worksheet in new_workbook._Workbook__worksheets if worksheet.name == sheet.name ]
#     
#         # Save the new_workbook based on sheet.name
#         new_workbook.save('{}_workbook.xls'.format(sheet.name))    
if __name__ == "__main__":
    main()