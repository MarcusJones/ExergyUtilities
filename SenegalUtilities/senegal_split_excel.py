
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
from win32com.client import Dispatch

from shutil import copyfile

import openpyxl

#https://msdn.microsoft.com/en-us/library/office/jj231257.aspx
#http://www.jkp-ads.com/Articles/Excel2007TablesVBA.asp

path_dir = r"C:\CesCloud Senegal PV\03 Working\Liste des villages\Fiche Enquete\10"
name_file = r"00 10 fiche enquete Goudiry Koulor Bani Israel.xlsx"

full_path = os.path.join(path_dir,name_file)
    
def main():
    print(full_path)

    workbook=openpyxl.load_workbook(full_path)
    
    sh_names = workbook.get_sheet_names()
    
    for sh_name in sh_names:
        print("processing:",sh_name)
        new_full_path = os.path.join(path_dir,'{}_split.xls'.format(sh_name))
        
        copyfile(full_path, new_full_path)
        print("Created:",new_full_path)
        
        new_workbook=openpyxl.load_workbook(full_path)
        
        new_sh_names = new_workbook.get_sheet_names()
        print(new_sh_names)
        for new_sh_name in new_sh_names:
            print("Sheet:",new_sh_name,end="")
            if new_sh_name == sh_name:
                print("... skipping:")
            else:
                print("... deleting:")
                sheet_to_delete = new_workbook.get_sheet_by_name(new_sh_name)
                new_workbook.remove_sheet(sheet_to_delete)
        new_workbook.save(new_full_path)
    print("Finished splitting",full_path)


if __name__ == "__main__":
    main()
    
    
    
if 0: # OLD    
    
    with util_xl.ExtendedExcelBookAPI(full_path) as xl:
        print(xl)
         
        #print()
         
        sheets = xl.get_sheet_names()
        #for i,sh in enumerate(sheets):
        #    print(i,sh)
         
        sheets = [(i,sh) for i,sh in enumerate(sheets)]
         
    print(sheets)
    for sheet_def in sheets:
        print(sheet_def)
        with util_xl.ExtendedExcelBookAPI(full_path) as xl:
            print(xl)
             
            #xl.write_book._Workbook__worksheets = [write_book._Workbook__worksheets[0]]
            
 
    exists = os.path.exists(full_path)
             
    excelPath = os.path.abspath(full_path)
    autosave = False
    logging.debug("Excel file at: {}, exists={}".format(excelPath,exists))
    xl = Dispatch('Excel.Application')
    xl.Visible = 1
    #raise
    book = xl.Workbooks.Open(excelPath)
    logging.debug("Excel book {}".format(book))
    raise
    for sheet in xl.book.Worksheets:
        print("Processing", sheet.name)
        for worksheet in xl.book.Worksheets:
            if worksheet.name == sheet.name:
                print("Skipping:",worksheet.name)
                this_sheet = worksheet
        print(this_sheet)
         
if 0:
 
    with util_xl.ExtendedExcelBookAPI(full_path) as xl:
        print(xl.book)
        xl.DisplayAlerts = False
        for sheet in xl.book.Worksheets:
            print("Processing", sheet.name)
            new_full_path = os.path.join(path_dir,'{}_split.xls'.format(sheet.name))
            #raise
            #new_workbook = copy.copy(xl.book)
            new_xl = xl.clone(new_full_path)
            #new_workbook.DisplayAlerts = False
            #raise
            #raise
            print("New excel API:",new_xl)
            #for worksheet in xl.book.Worksheets:
            print("New excel API, book:",new_xl.book)
            for worksheet in new_xl.book.Worksheets:
                if worksheet.name == sheet.name:
                    print("Skipping:",worksheet.name)
                    #this_sheet = worksheet
                else:
                    #sleep(0.05)
                    print("Deleting:",worksheet.name)
                    worksheet.Delete()
                    #worksheet.delete()
                    worksheet.Delete
                    worksheet.delete
                    #print(worksheet.Delete)
                    #print(worksheet.Delete())
            #new_workbook._Workbook__worksheets = [this_sheet]
            
            #new_workbook.append(this_sheet)
            
            print("NOW")
            for worksheet in new_xl.book.Worksheets:
                print(worksheet.name)
            
            #sleep(1)
            #new_workbook.Worksheets = [ worksheet for worksheet in new_workbook.Worksheets if worksheet.name == sheet.name ]
            #print(new_workbook)
            
            #new_full_path = os.path.join(path_dir,'{}_split.xls'.format(sheet.name))
            new_workbook.SaveAs(new_full_path)  
            new_workbook.Close(SaveChanges=0) # see note 1
            break
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