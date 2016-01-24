"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
import unittest
import os 

# Logging
import logging
logging.basicConfig(format='%(funcName)-20s %(levelno)-3s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")


# External 
import xlrd

# Own
from ExergyUtilities.utility_inspect import get_self, get_parent

#===============================================================================
# Testing
#===============================================================================

#===============================================================================
# Unit testing
#===============================================================================
#@unittest.skip("Skip")
class all_tests(unittest.TestCase):
    #@unittest.skip("Skip")
    def test010(self):
        print("**** TEST {} ****".format(get_self()))
        workBookPath = os.getcwd() + "\\..\\..\\TestingFiles\\testing01.xlsx"
        wb = xlrd.open_workbook(workBookPath)
        print("HELLO")
        print( wb)
        sh = wb.sheet_by_name(u'Sheet1')
        print( sh)
        for rownum in range(sh.nrows):
            print( sh.row_values(rownum))

    #@unittest.skip("Skip")
    def test020(self):
        print( "**** TEST {} ****".format(get_self()))

        workBookPath = os.getcwd() + "\\..\\TestingFiles\\testing01.xlsx"
        thisBook = ExcelBookRead(workBookPath)
        print( thisBook.get_table("Sheet1", 0, 2, 0, 2))
        thisTable = thisBook.get_table("Sheet1", 0, 2)
        for row in thisTable:
            for val in row:
                print( val)

    def test030(self):
        print( "**** TEST {} ****".format(get_self()))

        testPath = r"C:\Projects\IDFout\00Test.xlsx"
        testData= [['the', 'big', 'cat', 'flies'],[3,4,5]]
        xl = ExtendedExcelBookAPI(testPath)
        xl.write("testSht",testData)

        xl.write("testSht2",testData)

        nextRow = len(xl.get_table("testSht")) + 1
        xl.write("testSht",testData, nextRow)
        xl.save_and_close()


class test_pw(unittest.TestCase):
    def test010(self):
        print( "**** TEST {} ****".format(get_self()))
        workBookPath = r"C:\Users\PC1\Desktop\Test.xlsx"
        import sys
        #workBookPath = r"C:\Users\PC1\Desktop\short.xlsx"

        import win32com.client
        import itertools
        import string
        import traceback
        import datetime as dt
        import time
        xlApp = win32com.client.Dispatch("Excel.Application")
        print( "Excel library version:", xlApp.Version)

        for pw_size in range(5, 10):

            start_time = time.time()
            gen = itertools.combinations_with_replacement("123456789"+string.ascii_lowercase,pw_size)
            flg_found = False
            count = 0
            for password in gen:
                password = "".join(password)

                if count % 100 == 0:
                    print( "{:<10} - {}".format(count, password))


                try:
                    xlwb = xlApp.Workbooks.Open(workBookPath, 0, True, None, password)
                    flg_found = True
                except:
                    pass
                    #traceback.print(_exc()
                    #print( "Err"
                if flg_found:
                    break

                count += 1
            end_time = time.time()
            print( "Combinations length {} over {} seconds".format(pw_size,end_time - start_time))
            print( "Last password was {}".format(password))
            if flg_found:
                break

        print( password)
        print( password)
        print( password)




def _test1():
    logging.debug("Started _test1".format())


    thisExcelPath = os.path.normpath(r"..\smallprojects Definitions\testing1.xlsx")

    thisExcelPath = os.path.join(os.getcwd(), thisExcelPath)

    excelBook1 = ExtendedExcelBookAPI(thisExcelPath)

    excelBook1.scan_down("Variables", 1, 1, "Continous variables")

    excelBook1.scan_down("Variables", 7, 1, None)

    excelBook1.get_table("Variables", 1, 10, 1, 10)

    theseRows = excelBook1.get_rows("Variables", 1, None, 1, None)

    print( theseRows)

    logging.debug("Finished _test1".format())

