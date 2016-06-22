"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:


import unittest

# Logging
import logging
logging.basicConfig(format='%(funcName)-20s %(levelno)-3s: %(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
my_logger = logging.getLogger()
my_logger.setLevel("DEBUG")


# External 
#import xxx

# Own
from ExergyUtilities.utility_inspect import get_self, get_parent

#===============================================================================
# Testing
#===============================================================================
    
#===============================================================================
# Unit testing
#===============================================================================
class all_tests(unittest.TestCase):
    
    def setUp(self):
        print("**** TEST {} ****".format(get_self()))
        this_path = os.path.realpath(__file__) + r"\..\.."
        self.path = os.path.abspath(this_path)
        
        print(self.path)
        
    def test000_SimpleCreation(self):
        print("**** TEST {} ****".format(get_self()))
        text_file_path = os.path.join(self.path,"TestingFiles", "TestText.txt")
        print(text_file_path)
        
        this_obj = FileObject(text_file_path)
        this_obj.load_lines()
        this_obj.print_lines()
        
        print(this_obj)
        
        replacements = [[r"^WALL EXT_WALL$", "WALL REPLACED_WALL"],
                        [r"FRONT", "PIZZA"]]
        
        [
         [r"^WALL EXT_WALL$", "WALL REPLACED_WALL"],
        ]
        
        # After
        this_obj.make_replacements(replacements)
        this_obj.print_lines()
        
        print(this_obj.get_match("EXT_WALL"))
        
    def test010_filter1(self):
        get_files_by_name_ext(r'C:\newtestdir', "results", "csv")

    @unittest.skip("")
    def test010_Filter(self):
        print("**** TEST {} ****".format(get_self()))
        #print get_latest_rev_number(self.testDir,"","")
        print("Matches")
        matches = filter_files_dir(self.testDir)
        for path in matches:
            print(path)

        assert len(matches) == 6

        print("Matches")
        matches = filter_files_dir(self.testDir, ext_pat = "txt")
        for path in matches:
            print(path)

        assert len(matches) == 3

        print("Matches")
        matches = filter_files_dir(self.testDir, "text", ext_pat = "txt")
        for path in matches:
            print(path)

        assert len(matches) == 2
    @unittest.skip("")
    def test020_FilterRev(self):
        print("**** TEST {} ****".format(get_self()))
        #print get_latest_rev_number(self.testDir,"","")
        print(get_latest_rev(self.testDir, "text", ext_pat = "txt"))




        
def _test1():
    logging.debug("Started _test1".format())
    
    replace1 = SearchReplace("FIND1","Apples!!!!!!!!!!!!!!!!!!")
    replace2 = SearchReplace("FIND2","**********************BEACH(((((((((")
    
    replaceVector = [replace1, replace2]
    
    thisPath = r'D:\Freelancing\smallprojects Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\0.3_0.3_0.5_0.1_0.1_1.0_1.0_1.eso'
    thisPath = r'D:\Freelancing\smallprojects Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\\'
    thisPath = r"D:\Freelancing\TestFileObject\thisTestFile.txt"
    
    template = FileObject(thisPath)
    #newFileObj.loadAllText()
    #template.copy_to_full_path("Test2.text")
    
    workingFile = template.copy_to_same_dir("Test2.text")
    workingFile.make_replacements(replaceVector)
    
    logging.debug("Finished _test1".format())

def _test2():
    logging.debug("Started _test1".format())
    
    replace1 = ("FIND1","Apples!!!!!!!!!!!!!!!!!!")
    replace2 = ("FIND2","**********************BEACH(((((((((")
    
    replaceVector = [replace1, replace2]
    
    thisPath = r'D:\Freelancing\smallprojects Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\0.3_0.3_0.5_0.1_0.1_1.0_1.0_1.eso'
    thisPath = r'D:\Freelancing\smallprojects Expansion Test Dir2\0.3_0.3_0.5_0.1_0.1_1.0_1.0\\'
    thisPath = r"D:\Freelancing\TestFileObject\thisTestFile.txt"
    
    
    thisPathBase = r"D:\Freelancing\TestFileObject\\"
    thisPathSuffix = r"\0A Folder\Test55.text"
    
    template = FileObjectBaseSuffix(thisPathBase,thisPathSuffix)
    
    
    
    #print template
    #newFileObj.loadAllText()
    newFile = template.copyToNewBasePath("d:\\")
    
    #print newFile
    #workingFile = template.copy_to_same_dir("Test2.text")
    #workingFile.make_replacements(replaceVector)
    
    logging.debug("Finished _test1".format())

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
    
    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")
    
    logging.debug("Started _main".format())
    
    unittest.main()
    
    logging.debug("Finished _main".format())

