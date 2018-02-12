#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
#import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
#print(ABSOLUTE_LOGGING_PATH)
#logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
import os
import re
import codecs
#===============================================================================
#--- SETUP external modules
#===============================================================================
import pandas as pd

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self
import ExergyUtilities.util_path as util_path
#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================
def second_pass(path_base):
    #path_base = r"C:\Users\jon\Desktop\temp_boq2"
    
        #print(df.groupby(df['Comments']).agg(sum))

    #path_base_out = r"C:\Users\jon\Desktop\temp_boq2"
    files = util_path.get_files_by_name_ext(path_base, '.', 'csv')
    for f in files:
        logging.debug("File {}".format(f))
        
        this_dir, basename = os.path.split(f)
        #print(basename)
        #raise
        basename_noext, this_ext = os.path.splitext(basename)
        
        #print(f"{basename_noext}")
        logging.debug("Processing {}".format(basename_noext))
        df = pd.read_csv(f, sep=";")
        
        df = pd.read_csv(f, sep=";",encoding='utf_8')
        
         
        print(df.shape)
        print(df)
        #print(pd.to_numeric(df['Volume']))
        


        

def convert_units_to_floats(path_base, out_path):
    files = util_path.get_files_by_name_ext(path_base, '.', 'csv')
    
    for f in files:
        #logging.debug("File {}".format(f))
        
        this_dir, basename = os.path.split(f)

        basename_noext, this_ext = os.path.splitext(basename)
        
        logging.info("Processing {}, a {} from {} ".format(basename_noext, this_ext, path_base))
        
        # Load as DF
        df = pd.read_csv(f, sep=";",encoding='utf-8')
        
        logging.debug("Loaded as DF: {}".format(df.shape))

        # Converting
        df["Volume"] = pd.to_numeric(df["Volume"].str.extract(r"(\d+\.\d*)", expand=False))
        df["Area"] = pd.to_numeric(df["Area"].str.extract(r"(\d+\.\d*)", expand=False))
        if 'Elevation' in df:
            df["Elevation"] = pd.to_numeric(df["Elevation"].str.extract(r"(\d+\.\d*)", expand=False))

        logging.debug("Converted Volume Area Elevation".format())
        
        
        #print(os.access(out_path, os.R_OK),os.access('foo.txt', os.W_OK))
        this_out_path = os.path.join(out_path, basename_noext+'.csv')
        logging.debug("Writing DF to {}".format(this_out_path))
        
        df.to_csv(this_out_path, sep = ';')


def convert_all_to_utf(base_dir):
    files = util_path.get_files_by_name_ext(base_dir, '.', 'csv')
    for f in files:
        logging.debug("File {}".format(f))    
        util_path.force_utf_conversion(f)

if __name__ == "__main__":
    
    # FORCE TO UTF
    #base_dir = r"C:\Users\jon\Desktop\temp_BOQ"
    #convert_all_to_utf(base_dir)

    # GET FLOATS
    #base_dir = r"C:\Users\jon\Desktop\temp_BOQ"
    #out_dir = r"C:\Users\jon\Desktop\TEMP_BOQ3"
    #convert_units_to_floats(base_dir,out_dir)
    
    # GROUPING
    base_dir = r"C:\Users\jon\Desktop\TEMP_BOQ3"
    second_pass(base_dir)
