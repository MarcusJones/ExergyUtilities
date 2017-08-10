"""This is a regular module
"""

#--- SETUP Config
from config import *
import unittest

#--- SETUP Logging
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")
from utility_inspect import get_self

#--- SETUP Standard modules
#import logging
#import time
#import re 
#import datetime
import random

#--- SETUP 3rd party modules
import pandas as pd
#import numpy as np 
#import scipy.io as sio
#--- SETUP Custom modules


#===============================================================================
# Code
#===============================================================================
def create_frame(header_labels, headers, data, index=None):
    """A simple wrapper for pd.DataFrame instances
    """
    pd.set_option('display.multi_sparse', False)
    m_index = pd.MultiIndex.from_tuples(headers, names = header_labels)
    df = pd.DataFrame(data, columns=m_index, index = index)
    return df

@unittest.skip("")
class allTests(unittest.TestCase):
    
    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        print("**** {} ****".format(get_self()))
        # This is random

        data_2d = list()

        for i in range(5):
            row = [random.randint(0,10) for i in range(4)]
            data_2d.append(row)

        # This is fixed
        data_2d = [[1, "Chicken", "A", 6.0], [6, 2, "B", 3], [0, 8, "C", 7.5], [10, 6, "D", 8], [8, 2, "E", 0]]
        self.data_2d = list(zip(*data_2d))
        
        self.headerDef = ["Attrib1","Xpos","Ypos"]

        self.headers = [
                   ["alpha","beta","charlie","delta"],
                   ["0","2","2","4"],
                   ["0","1","1","6"],
                   ]
        
        
        
        #self.data_frame = pd.DataFrame(self.data_2d,)
        #self.header_frame = pd.DataFrame(self.headers, index=self.headerDef)
        
        print("asdfsdzf")
        
    def test010(self):
        print("**** TEST {} ****".format(get_self()))
        
        m_index = pd.MultiIndex.from_arrays(self.headers,names = self.headerDef)
        print(m_index)
        df = pd.DataFrame(data = self.data_2d, index = m_index)
        print(df)
        #return 

#@unittest.skip("")    
class allTests2(unittest.TestCase):
    
    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        print("**** {} ****".format(get_self()))
        # This is random

        # This is fixed
       
        self.header_def = ["Name","Nationality","City","Couple"]

        self.headers = [
                    ["Esther",    "Micheal" ,    "Marcus",    "Sabrina"],
                    ["Dutch", "Dutch",    "Canada", "Austria"],
                    ["Wien",    "Wien",    "Wien",    "Wien"],
                    [0,0,1,1]
                ]
        
        self.indices = ["Rent", "Fuel", "Food", "Beer"]
        
        data = [
            [-250,-250,-250,-250],
            [0,0,0,-80],
            [-120,-30,0,-180],
            [0,-137,0,0]
            ]
        self.data = list(zip(*data))

    def test020(self):
        print("**** TEST {} ****".format(get_self()))
        
        m_index = pd.MultiIndex.from_arrays(self.headers,names = self.header_def)
        print(m_index)
        df = pd.DataFrame(data = self.data, index = m_index, columns = self.indices)
        print("Basic")
        print(df.index)
        #print(df.)
        print(df)
        
        
        df = df.transpose()
        print()
        print("Transposed")
        print(df)
        #return 
