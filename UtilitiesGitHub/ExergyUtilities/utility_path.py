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

"""The :mod:`xx` module 
"""

#===============================================================================
# Set up
#===============================================================================
from __future__ import division
from __future__ import print_function

from config import *

# Standard
#import os
import re
#import time
from ExergyUtilities.utility_inspect import get_self, get_parent
import sys
import shutil
import errno
import unittest
#import zipfile, os.path

# Logging
import logging.config
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")


def e(pathName):
    """
    pathName is a desired path on drive for a project
    Will return a numbered version of this path
    """
    logging.info("Filtering {}".format(rootPath, name_pat, ext_pat, recurse))

    #print pathName
    pathName = os.path.normpath(pathName)
    fullPathList = split_up_dir(pathName)

    lastDirName = fullPathList.pop()
    rootPath = "".join(fullPathList)


    revisionList = list()

    for path in os.listdir(rootPath):

        thisImmediateSubDir = split_up_dir(path).pop()

        if re.findall("{}".format(thisImmediateSubDir), path):
            thisImmediateSubDir
            revisionTextList = re.findall("[\d]+", base)
            if revisionTextList:
                revisionText = re.findall("r[\d]+", base)[0]
                #print revisionText
                revisionNumber = int(re.findall("[\d]+",revisionText)[0])

                fileRevisionList.append((revisionNumber, filename))

    if not fileRevisionList:
        return None


    # Sort, and pop the most recent (last) filename
    #latestRevisionFileName = (sorted(fileRevisionList)).pop()[1]
    #latestRevisionFileNumber = (sorted(fileRevisionList)).pop()[1]
    #latestRevisionFileNamePath = os.path.join(sourceFileDir, latestRevisionFileName)

    return sorted(fileRevisionList).pop()[0]


    #revNum = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if revNum:
        revNum =  revNum + 1
        myFileName = myFileName + "_r" + "{0:02d}".format(revNum)
    else:
        myFileName = myFileName + "_r00"

    raise



def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            #print choice
            return valid[default]
        elif choice in valid:
            #print choice
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def create_dir(f):
    logging.debug("Creating {}".format(f))

    if not os.path.exists(f):
        os.makedirs(f)

def count_files(f):
    items = [os.path.join(f,name) for name in os.listdir(f)]
    return len([item for item in items if os.path.isfile(item)])

def count_dirs(f):
    items = [os.path.join(f,name) for name in os.listdir(f)]
    return len([item for item in items if os.path.isdir(item)])

def erase_dir(f):
    if query_yes_no("ERASING directory: {}, sure?".format(f), None):
        shutil.rmtree(f)

def erase_dir_contents(folder, flgEverything = True):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and  not flgEverything:
                os.unlink(file_path)
            else:
                os.unlink(file_path)
        except Exception, e:
            print(e)

def path_exists(f):
    if os.path.exists(f):
        return True
    if not os.path.exists(f):
        return False

def split_up_dir(pathName):
    pathName = os.path.normpath(pathName)
    logging.debug("Splitting {}".format(pathName))
    drive,path_and_file=os.path.splitdrive(pathName)
    path,thisFile=os.path.split(path_and_file)
    #print path, thisFile
    pureFileName,extension = os.path.splitext( thisFile)
    if extension:
        raise Exception("This is meant for directories, not files")

    folders=[]
    #folders.append(extension)
    folders.append(pureFileName)
    while 1:
        path,folder=os.path.split(path)
        #print path,folder
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)

            break

    folders.append(drive)
    folders.reverse()

    #print folders[-1]

    return folders

def split_up_path(pathName, flg_verbose = False):

    """
    """
    pathName = os.path.normpath(pathName)
    if flg_verbose:
        logging.debug("Splitting {}".format(pathName))
    drive,path_and_file=os.path.splitdrive(pathName)
    path,thisFile=os.path.split(path_and_file)
    pureFileName,extension = os.path.splitext( thisFile)
    folders=[]
    folders.append(extension)
    folders.append(pureFileName)
    while 1:
        path,folder=os.path.split(path)
        #print path,folder
        if folder!="":
            folders.append(folder)
        else:
            if path!="":
                folders.append(path)

            break

    folders.append(drive)
    folders.reverse()

    if flg_verbose:
        logging.debug("Result: {}".format(folders))

    return folders

def list_dirs2(root_path):
    return os.walk(root_path).next()[1]

def list_dirs(pathName):
    directories = list()
    for dirname in os.listdir(pathName):
        absPathName = os.path.join(pathName,dirname)
        #print pathName
        #print os.path.join(pathName, dirname)
        if os.path.isdir(absPathName):
            directories.append(absPathName)

    return directories

def get_most_recent_file(pathName):
    """From a directory, return the latest file by datetime
    """

    allFilePaths = list()
    for dirname, dirnames, filenames in os.walk(pathName):
        #for subdirname in dirnames:
        #    print os.path.join(dirname, subdirname)
        if filenames:
            for filename in filenames:
                thisFilePath = os.path.join(dirname, filename)
                allFilePaths.append(thisFilePath)

    greatestMtime = 0
    for filePath in allFilePaths:
            try:
                thisFileMtime = os.path.getmtime(filePath)
                if thisFileMtime > greatestMtime:
                    greatestMtime = thisFileMtime
            except:
                pass
    #print "last modified: {}".format(time.ctime(greatestMtime))
    return (pathName, greatestMtime)


def get_latest_revision(fullFilePath, verbose = False):
    """Take a full path as a signature, and search the dir for the latest revision file name

    """

    mySplitPath=  split_up_path(fullFilePath)
    myFileExt = mySplitPath.pop()
    myFileName = mySplitPath.pop()
    myFileDir = mySplitPath
    myDirString = "\\".join(myFileDir)
    #print myDir
    rev_num = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if not rev_num:
        raise Exception("Not found")

    myFileName = myFileName + "_r" + "{0:02d}".format(rev_num)

    completePathList = myFileDir +  [myFileName + myFileExt]
    fullFilePathREV = os.path.join(*completePathList)

    if verbose: 
        logging.info("Latest file: {}".format(fullFilePathREV))

    return fullFilePathREV

def get_new_file_rev_path(fullFilePath, verbose = False):
    """Takes the entire full file path, returns
    a new file name with an _r## added to the file name
    i.e. the string
    'C:\TestSQL\DSpaceTest.sql'  becomes
    'C:\TestSQL\DSpaceTest_r00.sql' becomes
    'C:\TestSQL\DSpaceTest_r01.sql' becomes
    etc.
    """

    mySplitPath=  split_up_path(fullFilePath)

    #myDir = "".join(mySplitPath[0:-3])

    myFileExt = mySplitPath.pop()
    myFileName = mySplitPath.pop()
    myFileDir = mySplitPath
    myDirString = "\\".join(myFileDir)
    #print myDir
    revNum = get_latest_rev_number(myDirString, myFileName, myFileExt)

    if revNum != None:
        revNum =  revNum + 1
    #os.path.exists(fullDBpath)

    if revNum:
        #print "YES"
        #fullDBpath = fullDBpath + "1"
        myFileName = myFileName + "_r" + "{0:02d}".format(revNum)
    else:
        myFileName = myFileName + "_r00"

    #firstPart = mySplitPath[0:-2]
    #secondPart = [mySplitPath[-2] + mySplitPath[-1]]
    #mySplitPath = firstPart + secondPart
    completePathList = myFileDir +  [myFileName + myFileExt]
    fullFilePathREV = os.path.join(*completePathList)
    if verbose:
        logging.info("New revision file: {}".format(fullFilePathREV))

    return fullFilePathREV

def get_files_by_name_ext(rootPath, search_name, search_ext):
    #print search_name
    #raise
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for this_name in files:
            thisFilePath = os.path.join(root, this_name)
            allFilePathList.append(thisFilePath)
    #print search_name
    # Filter
    resultFilePaths = list()
    #print allFilePathList

    for filePath in allFilePathList:
        #print os.path.splitext(filePath),
        basename = split_up_path(filePath,False)[-2]
        #print split_up_path(filePath)[-2]
        extension = split_up_path(filePath,False)[-1]
        #print search_name
        #print search_ext
        #print "Basename", basename
        #print "{}  {} {}".format(search_name, basename, re.match(search_name, basename))
        #print "{}  {} {}".format(search_ext, extension, re.search(search_ext, extension))
        #raise
        if re.search(search_name, basename) and re.search(search_ext, extension):
            #print filePath

            resultFilePaths.append(filePath)
#    resultFilePaths = [filePath for filePath in allFilePathList if
#                    os.path.splitext(filePath)[1].lower() == search_ext.lower() and os.path.basename(filePath) == search_name
#                    ]
#
    logging.info("Found {} {} file matching '{}' in {}".format(len(resultFilePaths),search_ext,search_name, rootPath))

    return resultFilePaths


def get_files_by_ext_recurse(rootPath,ext, ):
    ext = "." + ext

    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)


    # Filter
    resultFilePaths = list()

    resultFilePaths = [filePath for filePath in allFilePathList if
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]

    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))

    return resultFilePaths



def get_file_by_ext_one(rootPath,ext):
    ext = "." + ext

    # Walk the project dir
    allFilePathList = list()
    for item in os.listdir(rootPath):
        thisFilePath = os.path.join(rootPath, item)
        allFilePathList.append(thisFilePath)


    # Filter

    resultFilePaths = allFilePathList

    resultFilePaths = [filePath for filePath in resultFilePaths if
                    os.path.splitext(filePath)[1].lower() == ext.lower()
                    ]

    logging.info("Found {} {} files in {}".format(len(resultFilePaths),ext,rootPath))

    return resultFilePaths


def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


def filter_paths_by_filename(paths,filter):

    print(paths)
    # Walk the project dir
    allFilePathList = list()
    for root, dirs, files in os.walk(rootPath):
        for name in files:
            thisFilePath = os.path.join(root, name)
            allFilePathList.append(thisFilePath)

    #print


    #print [os.path.splitext(filePath) for filePath in paths]
    resultFilePaths = list()
    for filePath in paths:
        thisFileName = os.path.splitext(os.path.split(filePath)[1])[0]
        if thisFileName in filter:
            resultFilePaths.append(filePath)

#    raise
#    #fileNames = [os.path.split(filePath)[1] for filePath in paths]
#    print [os.path.splitext(os.path.split(filePath)[1]
#                                        )[0] for filePath in paths]
#    print filter
#    resultFilePaths = [filePath for filePath in paths if
#                       os.path.splitext(
#                                        os.path.split(filePath)[1]
#                                        )[0] in filter
#                    ]
#    print resultFilePaths
    logging.info("Filtered {} files out of {}".format(len(resultFilePaths),len(paths)))

    return resultFilePaths


def get_current_file_dir(this_file):
    return os.path.dirname(os.path.realpath(this_file))


def get_next_rev_number_dir(root_dir, sub_dir_name_searched):
    """Takes a directory, and a sub-directory
    Returns an integer
    """
    
    # Get all subdirectories in the root
    directories = list()
    for dirname in os.listdir(root_dir):
        abs_path = os.path.join(root_dir,dirname)
        if os.path.isdir(abs_path):
            directories.append(abs_path)
    
    sub_dirs = list()
    
    
    rev_num_list = list()
    for dir in directories:
        sub_dir = os.path.split(dir)[-1]
        #print(sub_dir)
        if re.search("{}[0-9]+".format(sub_dir_name_searched), sub_dir): 
            matched_rev_num = re.findall("[0-9]+".format(sub_dir_name_searched), sub_dir)[0]
            matched_rev_num = int(matched_rev_num)
            rev_num_list.append(matched_rev_num)
            #print(matched_rev_num)
            #print(re.findall("[\d]+",matched_sub_dir))
            #revision_number = int(re.findall("[\d]+",matched_sub_dir)[0])
            
            #sub_dirs.append(dir)
            #print(revision_number)
    #sub_dirs = [dir for dir in directories if re.search("{}".format(sub_dir_name_searched), dir)]
    
    #if not directories:
    #print(directories)    
    #print(sub_dirs)    
    #raise
    if not rev_num_list:
        return 0
    
    #print(rev_num_list)
    
    latest = sorted(rev_num_list).pop()
    next = latest + 1
    return next



def get_latest_rev_number(sourceFileDir, sourceFileName, extensionFilter, verbose = False):
    """Takes a directory, and a filter for extensions
    INCLUDING the period i.e.
    ".sql", ".idf"
    Returns an integer
    """
    fileRevisionList = list()
    for filename in os.listdir(sourceFileDir):
        #print filename, sourceFileName

        if re.findall("{}".format(sourceFileName), filename):
            base, extension = os.path.splitext(filename)
            if extension == extensionFilter:
                revisionTextList = re.findall("[\d]+", base)
                if revisionTextList:
                    revisionText = re.findall("r[\d]+", base)[0]
                    revisionNumber = int(re.findall("[\d]+",revisionText)[0])
                    fileRevisionList.append((revisionNumber, filename))

    if not fileRevisionList:
        return None
    latest = sorted(fileRevisionList).pop()[0]
    if verbose: 

        logging.info("Latest revision in {} - {}  - {}: {}".format(sourceFileDir, sourceFileName, extensionFilter, latest))

    return latest



#-- Update ----

def copy_file(src,dst):
    shutil.copyfile(src, dst)

    logString = "Copied {} to {}".format(src,dst)
    logging.debug(logString)

def filter_files_dir(rootPath, name_pat = ".", ext_pat = ".*", recurse = False, flg_verbose = False):
    """
    Filter files in a directory by name and extension
    """
    matches = list()

    for root, dirs, files in os.walk(rootPath):
        # Ensure we don't go into sub directories if recursion is off
        if rootPath == root and not recurse:
            # Loop over the files in this dir
            for fileName in files:
                this_name, this_ext = os.path.splitext(fileName)
                if re.search(name_pat, this_name) and re.search(ext_pat, this_ext):
                    #print root, this_name, this_ext
                    full_path = os.path.join(root, this_name+ this_ext)
                    matches.append(full_path)

                #thisFilePath = os.path.join(root, fileName)

                #print thisFilePath
        elif rootPath != root and not recurse:
            #print "skip"
            pass
        elif recurse:
            print("Recursion not yet supported")
            raise
        else:
            raise
    logging.info("Filtering {}, {}, {} - Recurse {}, found {}".format(rootPath,name_pat, ext_pat, recurse,len(matches)))
    return matches

def get_latest_rev(rootPath, name_pat = ".", ext_pat = ".*", recurse = False, flg_verbose = False):
    """
    Get latest revision full path
    """
    matches = filter_files_dir(rootPath, name_pat, ext_pat, recurse)
    revisionList = list()
    for fullPath in matches:
        if flg_verbose:
            print(fullPath)

        fName = split_up_path(fullPath)[-2]
        #print fName
        if re.search("[\d]+$", fName):
            revisionText = re.findall("[\d]+$", fName)[0]
            revisionNum = int(revisionText)
            revisionList.append((revisionNum, fullPath))


    if revisionList:
        lastRevPath = revisionList.pop()[1]
        logging.info("Last revision; {}".format(lastRevPath))

        return lastRevPath
    else:
        raise Exception("Couldn't find revisions in {} filename {} . {}".format(rootPath,name_pat,ext_pat))
        pass

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''): continue
                path = os.path.join(path, word)
            zf.extract(member, path)


class FileObject(object):
    def __init__(self,filePath):
        """
        File wrapper
        Needs a path
        """
        self.filePath =os.path.normpath(filePath) 
        #self.fileData = None
        self.lines = None
        logString = "Created {0}".format(self)
        logging.debug(logString)
        
        
#    def loadData(self):
#        #prin 'reading:', self.inputFileTemplatePath
#        input_file_handle = open(self.inputFilePath,'r')
#        # Don't read unicode... inputFileTemplate=unicode(input_file_handle.read(),'utf-8')
#        self.fileData=input_file_handle.read()
#        input_file_handle.close()
#        logString = "File data loaded for {0}".format(self)
#        logging.debug(logString)

#    def writeData(self):
#        outF = open(self.outputFilePath,'w')
#        outF.write(self.fileData)
#        outF.close()
#        # Free up that memory
#        self.fileData = "UNDEFINED"        
#        logString = "File data written for {0}".format(self)
#        logging.debug(logString)

    def __str__(self):
        return "File Object; exists={}, file={}, input path: {}".format(self.exists(), self.is_file(), self.filePath)
    
    def is_file(self):
        return os.path.isfile(self.filePath)
    
    def exists(self):
        #os.path.exists(self.filePath)
        return os.path.exists(self.filePath)
    
    def load_lines(self):
        if not self.exists():
            raise Exception("Problem on open; this file does not exist! ")
        elif not self.is_file():
            raise Exception("Problem on open; this is a directory! ")
        
        input_file_handle = open(self.filePath,'r')
        self.lines = input_file_handle.readlines()
        input_file_handle.close()

        logging.debug("{} lines of text loaded for {}".format(len(self.lines),self))        
        
    def load_all_text_OLD(self):
        """
        Load the text into memory
        """
        
        
        if not self.exists():
            raise Exception("Problem on open; this file does not exist! ")
        elif not self.is_file():
            raise Exception("Problem on open; this is a directory! ")
        
        input_file_handle = open(self.filePath,'r')
        
        # Don't read unicode... inputFileTemplate=unicode(input_file_handle.read(),'utf-8')
        self.fileData=input_file_handle.read().decode('ISO-8859-1')
        #self.fileData.decode()
        #self.fileData = self.fileData.encode('utf-8')
        input_file_handle.close()
        logString = "{} lines of text loaded for {}".format(len(self.fileData),self)
        logging.debug(logString)        

    def copy_to_same_dir(self,newFileName):
        """
        Copy the file in the path to a new path, create and return this new path
        as a new FileObject
        """
        #print "Basename:", os.path.basename(self.filePath)
        #print "Dirname:", os.path.dirname(self.filePath)
        #print "Realpath:", os.path.realpath(self.filePath)
        #print "Split:", os.path.splitext(self.filePath)
        #print "Extension:", os.path.splitext(self.filePath)[1]

        thisDirPath = os.path.dirname(self.filePath)
        targetPath = os.path.join(thisDirPath,newFileName)
        
        # =os.path.normpath(self.filePath) 
        shutil.copyfile(self.filePath, targetPath)
        #copyfile(ExergyUtilities, dst)
        
        return FileObject(targetPath)
        
    def copy_to_full_path(self,newPathName):
        """
        Copy the file in the path to a new path, create and return this new path
        as a new FileObject
        """        
        #print "Basename:", os.path.basename(self.filePath)
        #print "Dirname:", os.path.dirname(self.filePath)
        #print "Realpath:", os.path.realpath(self.filePath)
        #print "Split:", os.path.splitext(self.filePath)
        #print "Extension:", os.path.splitext(self.filePath)[1]
        
        # Could ensure that it exists (??)
        #if not os.path.exists(newPathName):
        #    raise Exception("This directory does not exist!")
        
        targetPath = newPathName
        
        # =os.path.normpath(self.filePath) 
        #print targetPath
        shutil.copyfile(self.filePath, targetPath)
        #copyfile(ExergyUtilities, dst)
        
        logString = "Copied {} to {}".format(self,newPathName)
        logging.debug(logString)
                
        return FileObject(targetPath)

    def print_lines(self,lines=None):
        for line in self.lines:
            print(line.strip())
    
    
    def write_file(self, outpath):
        
        #print(self.lines)
        outF = open(outpath,'w')
        
        outF.write("".join(self.lines))
        outF.close()
        
        logString = "Wrote {}".format(outpath)
        logging.debug(logString)
    
    def get_match(self,regexStr):
        matches = list()
        
        # First, make sure the file text is loaded 
        if not self.lines:
            self.load_lines()
        
        matched_line = None        
        for line in self.lines:
            thisMatch = re.search(regexStr,line,re.VERBOSE)
            if thisMatch:
                matched_line = thisMatch.group()
                break
        
        if not matched_line:
            raise Exception("Could not find {} in {}".format(regexStr,self))
            
        return matched_line

        
    def make_replacements(self,replacements):
        """replacements is a list of tuples, 
        
        """
        # replacements should be a list
        assert replacements[0][0]
        
        if isinstance(replacements, basestring):
            replacements = list().append(replacements) 
        
        # First, make sure the file text is loaded 
        if not self.lines:
            self.load_lines()

        # Search and sub for each replacement
        newLines = []
        
        for repl in replacements:
            repl.append(0)
        
        for line in self.lines:
            
            newLine = line
            # Check this line for all replacements
            for repl in replacements:
                #print(repl)
                # First check ahead if it matches anywhere
                #print(line)
                search_str = re.escape(repl[0]) 
                val_str = repl[1]
                match = re.findall(search_str, line)
                #print(match)
                if match:
                    repl[2] += 1
                    # Then do the sub
                    newLine = re.sub(search_str, val_str, newLine)
                    #print(newLine)
            # Append it
            newLines.append(newLine)
        #print(newLines)
        self.lines = newLines
        
        for repl in replacements:
            logging.debug("{} -> {} replaced in {} lines".format(repl[0], repl[1],  repl[2]))
        #print(self.lines)
#        for repl in replacements:
#            matchCount = 0
#            matchCount = 0
#            for line in self.lines:
#                match = re.search(repl[0], line)
#                if match:
#                    matchCount = matchCount + 1
#                newLines.append(re.sub(repl[0], str(repl[1]), line))
#        
        
    
    def make_replacementsOLD(self,replacements):
        """
        Reads the file data
        Make the given n replacements
        Writes the file again!
        Optimization: Currently makes n passes, could be just one!
        
        replate 
        """
        # replacements should be a list
        if isinstance(replacements, basestring):
            replacements = list().append(replacements) 
        
        # First, make sure the file text is loaded 
        if not self.fileData:
            self.loadAllText()
        #print self.fileData 
        
        # Now count the matches for all replacements
        matchCount = 0
        for repl in replacements:
            #print repl
            matches = re.findall(repl[0], self.fileData)
            #print self.fileData
            #matches = re.search("FIND1", self.fileData)
            #print matches
            #print len(matches)
            #print re.sub(repl.searchRegex, str(repl.replaceValue))
            matchCount = matchCount + len(matches)
        
        # Make sure we have at least one match
        if not matchCount:
            raise Exception("Not a single match in file! \n {} \n {}".format(self,replacements))
        
        # We could also limit the maximum number of matches
        elif matchCount > 1:
            pass
            #raise Exception("More than one match ({}) for {}".format(len(matches),matches))

        # Search and sub for each replacement
        for repl in replacements:
            self.fileData = re.sub(repl[0], str(repl[1]), self.fileData)
        logString = "{} replacement for {}".format(matchCount, self)
        logging.debug(logString)

class FileObjectBaseSuffix(FileObject):
    def __init__(self,baseFilePath,suffixFilePath):
        """
        File wrapper
        Needs a path
        """
        #print baseFilePath, suffixFilePath
        filePath =os.path.normpath(baseFilePath+suffixFilePath) 
        #print filePath
        self.baseFilePath = baseFilePath
        self.suffixFilePath = suffixFilePath
        
        super(FileObjectBaseSuffix, self).__init__(filePath)
    
    def changeBase(self,newBasePath):
        self.filePath = os.path.join(newBasePath,self.suffixFilePath) 
        
    def changeSuffix(self,newSuffixPath):
        self.filePath = os.path.join(self.baseFilePath,newSuffixPath) 

    def copyToNewBasePath(self,newBasePath):
        """
        Copy the file in the path to a new base, create and return this new path
        as a new FileObject
        """        
        newPathName = os.path.join(newBasePath,self.suffixFilePath) 
        targetPath = newPathName
        

        newDirectoryPath = os.path.dirname(newPathName)
        
        # Make the directory tree if doesn't exist
        try:
            os.makedirs(newDirectoryPath)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        shutil.copyfile(self.filePath, targetPath)
        #copyfile(ExergyUtilities, dst)
        
        return FileObjectBaseSuffix(newBasePath,self.suffixFilePath)
