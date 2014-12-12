"""This is a testing module
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function
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

@unittest.skipIf(0,"")
class test_simple_load(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
    def test010_simple_load(self):
        print "**** TEST {} ****".format(whoami())

        path_file = r"M:\52_CES\14011_LEED_MediaTower\4_Doks\41_Ein_Doks\140603 Site visit MJ FB\A_01_MV_KM1_KM1.Power_anz\2009032809.txs"

        load_database(path_file)


@unittest.skipIf(1,"")
class testDataBase(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

        myLogger.setLevel("CRITICAL")


        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]

        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace

        myLogger.setLevel("DEBUG")

    def test010_(self):
        testLocation = "C:\TestSQL\update.sql"
        metadata, engine = createTables(self.D1,":memory:")
        populateTableDSpace(metadata, engine,self.D1)


        #print "Table names:"
        #print metadata.tables.keys()
        #variablesTable = metadata.tables["variables"]



        someResults = (
                       (-37584290, datetime.datetime.now(), datetime.datetime.now(), 1, 1, 1, 1),
                       (-37584230, datetime.datetime.now(), datetime.datetime.now(), 1, 1, 1, 2),
                       )

        #theResult =
        insertRows(engine, metadata.tables["results"],someResults )


        print_all_pretty_tables(engine, metadata)