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



#===============================================================================
#---TESTING---------------------------------------------------------------------
#===============================================================================
@unittest.skipIf(1,"")
class testIdfSQL(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        #fullPath = r"C:\Users\PC1\Desktop\TCJ_A4_ehb.sql"

        self.excel_path_all_tables = os.path.join(SAMPLE_SQL,"test_all_tables.xlsx")
        self.excel_path_vector_table = os.path.join(SAMPLE_SQL,"test_vectors.xlsx")

        self.RVDD_path = os.path.join(SAMPLE_SQL,"rvdd.xlsx")

        fullPath = os.path.join(SAMPLE_SQL,"Proposed2.sql")

        #\MyUtilities
        #fullPath = r"C:\Projects\Simulation\TCJ_A3_ene v8.sql"
        self.engine = sa.create_engine('sqlite:///{}'.format(fullPath), echo=ECHO_ON, listeners=[ForeignKeysListener()])
        logging.info("Connected to {} ".format(fullPath))

        self.metadata = sa.MetaData()
        self.metadata.reflect(self.engine)

    @unittest.skipIf(0,"")
    def test010_get_column(self):
        print "**** TEST {} ****".format(whoami())
        table_name = u'ReportVariableDataDictionary'
        table_obj = get_table_object(self.metadata, table_name)
        column_name = "VariableType"
        col = get_column(table_obj,column_name)
        print "Returned column {} from table {}".format(column_name,table_name)
        print col

    @unittest.skipIf(1,"")
    def test020_pretty_print(self):
        #printOnePrettyTable(self.engine,"ReportVariableData",maxRows = 200)
        #printOnePrettyTable(self.engine,"Time",maxRows = 200)
        printOnePrettyTable(self.engine,"ReportVariableDataDictionary",maxRows = 200)
        #printOnePrettyTable(self.engine,"ReportVariableExtendedData",maxRows = 200)


    @unittest.skipIf(1,"")
    def test020_frame(self):
        print "**** TEST {} ****".format(whoami())

        #ReportVariableDataDictionary
        #get_frame_Eplus(self.engine,self.metadata)

        fr_zones = get_frame_simple(self.engine,self.metadata,"Zones")
        #print(fr_zones)
        print("First 3 zone names : \n{} ".format(fr_zones['ZoneName'][:3]))

        #print(fr_zones[:3, 'ZoneName'])
        fr_zones.to_excel(r"C:\temp\tes.xls")


    @unittest.skipIf(0,"")
    def test010_printTables(self):
        print "**** TEST {} ****".format(whoami())

        print("\nTables")
        print("---------")
        print([table for table in get_table_names(self.metadata)])
        #for table in get_table_names(self.metadata):
        #    print table,


        print("\nRVDD")
        print("---------")
        t_RVDD = get_table_object(self.metadata, u'ReportVariableDataDictionary')
        print("Report dictionary table object: {} , {}".format(t_RVDD, type(t_RVDD)))
        print("Report dictionary table columns: {}".format(t_RVDD.c))
        var_names = idf_var_names_RVDD(self.engine,self.metadata)
        print("{} Variables in RVDD, from {} to {}".format(len(var_names), var_names[0], var_names[-1] ))

        print("\nZones")
        print("---------")
        t_zones = get_table_object(self.metadata, u'Zones')
        print("Zones: {} , {}".format(t_zones, type(t_zones)))
        print("Zones columns: {}".format(t_zones.c))

        print("Zones count: {}".format(count_rows(self.engine,t_zones)))
        print("Zones rows: {}".format(get_rows(self.engine,t_zones)[0]))



        #var_names = idf_var_names_RVDD(self.engine,self.metadata)
        #print("{} Variables in RVDD, from {} to {}".format(len(var_names), var_names[0], var_names[-1] ))


        #printOnePrettyTable(self.engine, u'ReportVariableDataDictionary')

        #for item in t_RVDD:
        #    print item

        #printOnePrettyTable(self.engine, "Constructions")
        #printOnePrettyTable(self.engine, "Surfaces",100)

        #print_all_pretty_tables(self.engine,maxRows = 10)
        #print("---------")

        #print("{}".format(len(var_names))
        #for v_name in var_names:
        #    print v_name






    @unittest.skipIf(1,"")
    def test100_get_vectors(self):
        print "**** TEST {} ****".format(whoami())
        """VariableType    IndexGroup    TimestepType    KeyValue    VariableName    ReportingFrequency    ScheduleName    VariableUnits"""

        #tbl_rvdd = get_table_object(self.metadata, "ReportVariableDataDictionary")

        #printOnePrettyTable(self.engine,"ReportVariableDataDictionary",maxRows = 200)

        vector_list = list()
        # Get the raw vectors
        for criteria in VECTOR_SET:

            vector = get_variable_vector(self.engine, self.metadata,criteria)
            #print vector
            vector_list.append(vector)

        # Assemble the data
        headers = list()
        data = list()
        for vector in vector_list:
            data.append(vector.pop())
            headers.append(vector.pop())

        #print data
        #print zip(*data)
        #raise
        header_def = ["name","key","units"]

        this_frame = xrg.ExergyFrame(
                name="Test",
                dataArray = zip(*data),
                timeArray=None,
                headersArray = zip(*headers),

                headersDef= header_def,
                )
        this_frame = xrg.add_simple_time(this_frame)
        print this_frame.checkTimeExists()
        xrg.displayFrame(this_frame)


    @unittest.skipIf(1,"")
    def test100_get_vectorsOLD(self):

        assert(df.shape[1] == 1), "Too many columns returned from criteria:{}".format(criteria)
        df_list.append(df)



        header_def = ["name","key","units"]

        frame_list = list()
        for df in df_list:
            variable_names = df["VariableName"][0]
            variable_units = df["VariableUnits"][0]
            variable_keys = df["KeyValue"][0]

            header = [variable_names, variable_units, variable_keys]
            #df.pop('VariableName')
            #df.pop('VariableUnits')
            #df.pop('KeyValue')
            #df.pop('ReportingFrequency')
            print header
            raise
            this_frame = xrg.ExergyFrame(
                name="Test",
                dataArray = df["VariableValue"].values,
                timeArray=df.index,
                headersArray=header,

                headersDef= header_def,
                )
            frame_list.append(this_frame)


        for frame in frame_list:
            frame.checkShapes()
            #xrg.displayFrame(frame)
            #print xrg.displayFrame(frame)
            #checkShapes

        new_frame = xrg.mergeFrames("results", frame_list, flgMergeHeads = False)
        new_frame = xrg.add_simple_time(new_frame)
        xl = ExtendedExcelBookAPI(self.excel_path_vector_table)

        new_frame.saveToExcelAPI(xl,'Comparison')
        xl.save_and_close()
        xl.closeAll()


    @unittest.skipIf(1,"")
    def test010_cycleAll(self):
        print "**** TEST {} ****".format(whoami())

        #ReportVariableDataDictionary
        get_frame_Eplus(self.engine,self.metadata)

    @unittest.skipIf(1,"")
    def test010_getVectorOLD(self):
        print "**** TEST {} ****".format(whoami())

        var_name = "Zone Infiltration Sensible Heat Loss"

        key_value = "A4%3NP:3NP%OFFICE%NORTH"

        print get_variable_def_from_RVDD(self.engine,self.metadata,var_name,key_value)
        get_variable_vector(self.engine,self.metadata,6)
        #, varName, key_val


    @unittest.skipIf(1,"")
    def test300_write_RVDD(self):
        print "**** TEST {} ****".format(whoami())
        max_rows = None
        writer = pd.ExcelWriter(self.RVDD_path)
        fr = get_frame_simple(self.engine,self.metadata,"ReportVariableDataDictionary",max_rows)

        print("Writing {}, {} rows".format("ReportVariableDataDictionary", len(fr)))

        #print(fr_zones[:3, 'ZoneName'])
        fr.to_excel(writer,"ReportVariableDataDictionary")

        writer.save()



    @unittest.skipIf(1,"")
    def test300_export_all_to_excel(self):
        print "**** TEST {} ****".format(whoami())
        max_rows = 1000
        writer = pd.ExcelWriter(self.excel_path_all_tables)
        for table_name in [table for table in get_table_names(self.metadata)]:
            fr = get_frame_simple(self.engine,self.metadata,table_name,max_rows)

            print("Writing {}, {} rows".format(table_name, len(fr)))

            #print(fr_zones[:3, 'ZoneName'])
            fr.to_excel(writer,table_name)

        writer.save()

    @unittest.skipIf(1,"")
    def test010_printResults(self):
        print "**** TEST {} ****".format(whoami())
        printOnePrettyTable(self.engine, "ReportVariableData",100)
        #printOnePrettyTable(self.engine, "ReportVariableDataDictionary",10)

        #printOnePrettyTable(self.engine, "Time",100)


        #thisTable = get_table_object(self.metadata, "ReportVariableDataDictionary")

        tReportVariableData = get_table_object(self.metadata, "ReportVariableData")
        tReportVariableDataDictionary = get_table_object(self.metadata, "ReportVariableDataDictionary")
        tTime = get_table_object(self.metadata, "Time")

        for item in dir(get_table_object(self.metadata, "ReportVariableDataDictionary")):
            print item
        print type(tReportVariableData)
        print tReportVariableData.columns
        print tReportVariableData.count
        print tReportVariableData.join
        print tReportVariableData.foreign_keys
        print tReportVariableData.primary_key
        #print tReportVariableData.__table_args__
        #tReportVariableData.join(tTime)
        #raise
        """
        SELECT column_name(s)
        FROM table1
        INNER JOIN table2
        ON table1.column_name=table2.column_name;
        """



        qry = tReportVariableData.join(tTime, tReportVariableData.c.TimeIndex  == tTime.c.TimeIndex)

        qry = sa.join(tReportVariableData,tTime,tReportVariableData.c.TimeIndex  == tTime.c.TimeIndex)

        qry = qry.select()

        #qry = sa.select(from_obj = qry )
        #results = self.engine.execute(qry)
        #print qry
        print type(qry)
        print qry
        results = self.engine.execute(qry)


        print results
        for res in results:
            print res
        raise
        #join(right, onclause=None, isouter=False)


        RAW_SQL = """
        ALTER TABLE Employees
        ADD FOREIGN KEY (UserID)
        REFERENCES ActiveDirectories(id)
        """
        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD CONSTRAINT FK_TimeIndex_Time FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD CONSTRAINT PerOrders
        FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData"""

"""
***ReportVariableData***
+-----------+-----------------------------------+------------------+---------------------------------+
| TimeIndex | ReportVariableDataDictionaryIndex |  VariableValue   | ReportVariableExtendedDataIndex |
+-----------+-----------------------------------+------------------+---------------------------------+
|     1     |                 6                 | -0.0583333333333 |               None              |
|     1     |                 7                 |      -1.95       |               None              |
"""

"""
***ReportVariableDataDictionary***
+-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
| ReportVariableDataDictionaryIndex | VariableType | IndexGroup | TimestepType |          KeyValue         |             VariableName            | ReportingFrequency | ScheduleName | VariableUnits |
+-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
|                 6                 |     Avg      |    Zone    |     Zone     |        Environment        |           Outdoor Dry Bulb          |       Hourly       |     None     |       C       |
"""


"""
***Zones***
+-----------+-----------------------------+----------+---------+---------+---------+----------------+----------------+---------------+--------+------------+----------------+----------------+----------------+-----------------+-----------------+----------+----------+---------------+---------------+----------------------+-----------------------+-----------+------------------+----------------+---------------+-------------------+
| ZoneIndex |           ZoneName          | RelNorth | OriginX | OriginY | OriginZ |   CentroidX    |   CentroidY    |   CentroidZ   | OfType | Multiplier | ListMultiplier |    MinimumX    |    MaximumX    |     MinimumY    |     MaximumY    | MinimumZ | MaximumZ | CeilingHeight |     Volume    | InsideConvectionAlgo | OutsideConvectionAlgo | FloorArea | ExtGrossWallArea | ExtNetWallArea | ExtWindowArea | IsPartOfTotalArea |
+-----------+-----------------------------+----------+---------+---------+---------+----------------+----------------+---------------+--------+------------+----------------+----------------+----------------+-----------------+-----------------+----------+----------+---------------+---------------+----------------------+-----------------------+-----------+------------------+----------------+---------------+-------------------+
|     1     |  A4%1NPA:1NPA%OFFICE%NORTH  |   0.0    |   0.0   |   0.0   |   0.0   | -17.1730861826 | -33.0571134869 | 2.05999999685 |   1    |    1.0     |      1.0       | -23.5490771482 | -12.7021670377 |  -38.1740888444 |  -30.0069178664 |   0.0    |   4.12   |      4.12     | 156.555857223 |          2           |           7           |  41.7482  |  47.5573685367   | 42.1173685367  |     4.978     |         1         |

"""

"""
***Time***
+-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
| TimeIndex | Month | Day | Hour | Minute | Dst | Interval | IntervalType | SimulationDays | DayType | EnvironmentPeriodIndex | WarmupFlag |
+-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
|     1     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |
|     2     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |

"""
