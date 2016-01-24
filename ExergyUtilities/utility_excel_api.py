# ExergyUtilities
# Copyright (c) 2010, B. Marcus Jones <>
# All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`xx` module is a utility and notebook module to interface with Excel. This is a pure API implementation. 
For xlrd/xlwt methods, see utility_excel module. 
"""




from win32com.client import Dispatch
import logging.config
import os
import re

import shutil

class ExtendedExcelBookAPI(object):
    """A pure API implementation of Excel interfacing
    No external modules required. 
    Implements 'with' scope constructor.
    
    """

    def __enter__(self):
        logging.debug("***Enter***".format())
        return self

    def __exit__(self, type, value, traceback):
        logging.debug("***Exit***".format())
        if self.autosave:
            self.save_and_close()
        else:
            self.closeAll()
            
    def __init__(self, excelPath, autocreate = False, autosave = False):
        self.excelPath = os.path.abspath(excelPath)
        self.autosave = autosave
        logging.debug("Excel file at: {}, exists={}".format(self.excelPath,self.exists))
        self.xl = Dispatch('Excel.Application')
        self.xl.Visible = 0
        
        if not self.exists and autocreate:
            self.book = self.xl.Workbooks.Add()
            #print self.xl
            #print self.xl.Workbooks.Add()
            #print self.book
            print(self.book)
            print(self.excelPath)
            self.book.SaveAs(self.excelPath)
            logging.debug("Created file Excel file at: {}, exists={}".format(self.excelPath,self.exists))
        else:
            self.book = self.xl.Workbooks.Open(self.excelPath)
    
    def closeAll(self):
        #self.book.Close(0)
        self.xl.Quit()

    def saveAs(self):
        self.xl.ActiveWorkbook.SaveAs(self.excelPath)

    def save(self):
        self.xl.ActiveWorkbook.Save()

    def save_and_close(self):
        self.xl.ActiveWorkbook.SaveAs(self.excelPath)
        self.xl.ActiveWorkbook.Close(SaveChanges=0) # see note 1
        logging.debug("Closed excel file at: {}".format(self.excelPath))

    def save_and_close_no_warnings(self):
        self.xl.DisplayAlerts = False
        self.xl.ActiveWorkbook.SaveAs(self.excelPath)
        self.xl.ActiveWorkbook.Close(SaveChanges=0) # see note 1
        logging.debug("Closed excel file at: {}".format(self.excelPath))
        
    def sheet_exists(self,sheetName):
        for sheet in [name.Name for name in self.book.Sheets]:
            if sheet == sheetName:
                return True
        return False

    def get_last_row(self,sheetName):
        sh = self.book.Sheets[sheetName]
        return sh.get_rows()
    
    def write_one(self,sheet_name, rownum,colnum, value):
        # Select the sheet
        sheet = self.book.Sheets(sheet_name)
        
        sheet.Cells(rownum,colnum).Value = value
        
        logging.debug("Wrote {} to {} {} {}".format(value,sheet_name,rownum,colnum))
        
    def write(self,sheetName,rows,x=0,y=0):

        assert( type(rows[0]) == list or type(rows[0]) == tuple), "Need a 2D array {} = {}".format(type(rows[0]), rows[0])
        LIMIT_SHEET_NAME = 20
        if len(sheetName) > LIMIT_SHEET_NAME:
            sheetName = sheetName[0:LIMIT_SHEET_NAME]
        sheetName = sheetName.replace(":", " ")

        #print self.sheet_exists(sheetName)
        #print [name.Name for name in self.book.Sheets]
        #print [name.Name for name in self.book.Worksheets]
        #prin
        if self.sheet_exists(sheetName):
            # Use the existing
            sh = self.book.Sheets[sheetName]
            logging.debug("Sheet {} exists".format(sheetName))

        else:
            # Create a new, rename it
            sh = self.book.Worksheets.Add()
            #lastSheet = self.book.Sheets.Count
            #sh = self.book.Sheets[lastSheet-1]
            try:
                sh.Name = sheetName
            except:
                print(sheetName)
                print(sheetName.__str__)
                raise
            sh = self.book.Sheets[sheetName]
            logging.debug("Sheet {} created".format(sheetName))


        # Iterate over data
        for i,row in enumerate(rows):
            i += 1 + x
            
            for j,item in enumerate(row):
                j+=1 + y
                sh.Cells(i,j).Value = item

        #self.save_and_close()

        """
        >>> from win32com.client import Dispatch
        >>> app = Dispatch('Excel.Application')
        >>> app.Visible = True
        >>> wrk = app.Workbooks.Add()
        >>> wrk.Sheets.Count
        3
        >>> sh = wrk.Sheets.Add()
        >>> wrk.Sheets.Count
        4
        >>> sh.Name
        u'Sheet4'
        >>> sh.Name = 'New Name 4'
        >>> wrk.Sheets[0].Name
        u'New Name 4'
        >>> wrk.Sheets[2].Name
        u'Sheet2'
        >>> wrk.Sheets[2].Name = 'Hello'
        >>> wrk.Save()
        >>> wrk.Close(0)
        >>> app.Quit()
        """

        """

        import win32com.client
        xlApp = win32com.client.Dispatch("Excel.Application")
        xlApp.Visible=1
        xlWb = xlApp.Workbooks.Open("Read.xls")
        print xlApp.Worksheets("Sheet1").Name
        xlApp.Worksheets("Sheet2").Range("A1").Value = "yellow"
        cell = xlApp.Worksheets("Sheet3")
        cell.Range("C3").Value = "money"
        cell.Range("D4").Value = 9999
        print cell.Range("C3").Value
        print cell.Range("D4").Value
        xlWb.Close(SaveChanges=1)
        xlApp.Quit()
        """


        #$print book
        #raise

        # create new file ('Workbook' in Excel-vocabulary)


#        # store default worksheet object so we can delete it later
#        defaultWorksheet = workbook.Worksheets(1)
#
#        # build new chart (on seperate page in workbook)
#        chart = workbook.Charts.Add()
#        chart.ChartType = constants.xlXYScatter
#        chart.Name = "Plot"
#
#        # create data worksheet
#        worksheet = workbook.Worksheets.Add()
#        worksheet.Name = "Plot data"
#
#        # install data
#        xColumn = addDataColumn(worksheet, 0, x)
#        yColumn = addDataColumn(worksheet, 1, y)
#
#        # create series for chart
#        series = chart.SeriesCollection().NewSeries()
#        series.XValues = xColumn
#        series.Values = yColumn
#        series.Name = "Data"
#        series.MarkerSize = 3
#
#
#
#

        self.save()
        logging.debug("Wrote {} rows to Excel file at: {}, sheet {}, starting at row {}".format(len(rows),self.excelPath,sheetName,x))


    def clone(self,new_path):
        shutil.copy(self.excelPath,new_path)
        return ExtendedExcelBookAPI(new_path)

    @property
    def exists(self):
        return os.path.exists(self.excelPath)


    def get_sheet_names(self):
        xl = Dispatch('Excel.Application')


        sheetObjects = self.book.Worksheets
#
#        print
#
#        for sht in sheets:
#            print sht.Name
        sheets = [sht.Name for sht in sheetObjects]
        #print sheets

        logging.debug("Found {} sheet names".format(len(sheets)))

        return sheets

    def scan_down_2(self, targetSheet, rowNumber, colNumber, searchString, limitScan=1000):
        """
        Pass in searchString="None" to find the next empty cell
        (As an actual string, not python None type
        Limit is 1000 rows as default
        """

        logging.debug("Scanning {}, column {}, starting row {}, for '{}'".format(targetSheet, rowNumber, colNumber, searchString))

        # Select the sheet
        sheet = self.book.Sheets(targetSheet)

        #xl.Visible = False

        # Scan down
        thisRow = rowNumber
        foundRow = None
        for row in range(rowNumber,limitScan):
            currentValue = sheet.Cells(row,colNumber).Value
            # Look for it
            #print currentValue,searchString
            #print currentValue
            #print searchString
            #print re.search(currentValue,searchString)
            currentValue = str(currentValue)
            if currentValue and searchString and re.search(searchString,currentValue):
                foundRow = thisRow
                break
            if not currentValue and not searchString:
                foundRow = thisRow
                break
            thisRow += 1

        #book.Close(SaveChanges=0) #to avoid prompt

        if foundRow:
            logging.debug("Found {} at row {}, column {}".format(searchString, foundRow, colNumber))
            return foundRow
        else:
            raise Exception("{} not found".format(searchString))



    def scan_down(self, targetSheet, rowNumber, colNumber, searchString, limitScan=1000):
        """
        Pass in searchString=None to find the next empty cell
        Limit is 1000 rows as default
        """

        logging.debug("Scanning {}, column {}, starting row {}, for '{}'".format(targetSheet, rowNumber, colNumber, searchString))

        # Attach the excel COM object

        xl = Dispatch('Excel.Application')

        # Open the project file
        book = xl.Workbooks.Open(self.excelPath)

        # Select the sheet
        sheet = book.Sheets(targetSheet)

        xl.Visible = False

        # Scan down
        thisRow = rowNumber
        foundRow = None
        for row in range(rowNumber,limitScan):
            currentValue = sheet.Cells(row,colNumber).Value
            # Look for it
            #print currentValue,searchString
            #print currentValue
            #print searchString
            #print re.search(currentValue,searchString)
            currentValue = str(currentValue)
            if currentValue and searchString and re.search(searchString,currentValue):
                foundRow = thisRow
                break
            if not currentValue and not searchString:
                foundRow = thisRow
                break
            thisRow += 1

        book.Close(SaveChanges=0) #to avoid prompt

        if foundRow:
            logging.debug("Found {} at row {}, column {}".format(searchString, foundRow, colNumber))
            return foundRow
        else:
            raise Exception("{} not found".format(searchString))

    def get_rows(self, targetSheet, startRow=1, endRow = 1000, startCol=1,endCol = 100):
        """
        Return cols until first blank
        """
        #logging.debug("Loading project from {0}".format(self.excelPath))

        # Attach the excel COM object

        xl = Dispatch('Excel.Application')

        # Open the project file
        book = xl.Workbooks.Open(self.excelPath)

        # Select the sheet
        sheet = book.Sheets(targetSheet)

        xl.Visible = False

        rows = list()

        if not endRow:
            runUntilRow = 1000
        else:
            runUntilRow = endRow

        if not endCol:
            runUntilCol = 100
        else:
            runUntilCol = endCol

        checks = 0

        for row in range(startRow,runUntilRow+1):
            col = 1

            #?? What is this?
            if not endRow and not sheet.Cells(row,col).Value:
                break

            # Only return non-empty rows!
            if sheet.Cells(row,col).Value is None:
                pass
            else:
                rows.append(list())

            for col in range(startCol, runUntilCol+1):
                checks += 1
                thisVal = sheet.Cells(row,col).Value
                #print checks, thisVal
                if thisVal is not None:
                    rows[-1].append(thisVal)

        book.Close(SaveChanges=0) #to avoid prompt

        logging.debug("Checked {} cells".format(checks))
        logging.debug("Returning {} rows".format(len(rows)))

        return rows

    def get_cell(self, targetSheet, row, col):
        xl = Dispatch('Excel.Application')

        # Open the project file
        book = xl.Workbooks.Open(self.excelPath)

        # Select the sheet
        sheet = book.Sheets(targetSheet)

        xl.Visible = False

        thisVal = sheet.Cells(row,col).Value

        book.Close(SaveChanges=0) #to avoid prompt

        logging.debug("Returning '{}' at row {}, col {} in sheet {} ".format(thisVal, row, col,targetSheet ))

        return thisVal


    def get_table_2(self, targetSheet, startRow, endRow, startCol, endCol):
        """
        startRow, Starts at 1, not 0!
        endRow, Inclusive
        startCol, Starts at 1
        endCol Inclusive
        """
        logging.debug("Loading table on {}".format(targetSheet))

        # Attach the excel COM object

        xl = Dispatch('Excel.Application')

        # Open the project file
        book = xl.Workbooks.Open(self.excelPath)

        # Select the sheet
        sheet = book.Sheets(targetSheet)

        xl.Visible = False

        rows = list()
        for row in range(startRow,endRow+1):
            rows.append(list())
            for col in range(startCol, endCol+1):
                thisVal = sheet.Cells(row,col).Value
                rows[-1].append(thisVal)

        book.Close(SaveChanges=0) #to avoid prompt

        return rows

#     def get_table(self,sheetName):
#         table = ExcelBookRead(self.excelPath).get_table(sheetName)
# 
#         logging.debug("Got table len {} from sheet {}".format(len(table),sheetName))
# 
#         return table


# class BaseExcelAPI:
#     def __enter__(self,excelPath):
#         self.object = ExtendedExcelBookAPI(excelPath)
#         return self.object
#     
#     def __exit__(self, type, value, traceback):
#         self.object.save_and_close()
