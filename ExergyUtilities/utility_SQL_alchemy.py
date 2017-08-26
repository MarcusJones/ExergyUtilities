#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B.
Etc.
metadata sqlalchemy.schema.MetaData
engine acts as an interface
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:


from config import *

import logging.config
import unittest
from ExergyUtilities.utility_excel_api import ExtendedExcelBookAPI

from .utility_inspect import get_self, get_parent
import datetime
from ExergyUtilities.utility_path import get_new_file_rev_path
from UtilityPrintTable import PrettyTable
import pandas as pd
#from exergyframes import exergy_frame as xrg

import sqlalchemy as sa
#from sqlalchemy import Table, Column, Integer, String, ForeignKey,DateTime, Boolean, MetaData

import datetime

ECHO_ON = False

from sqlalchemy.interfaces import PoolListener

VECTOR_SET = [
              (('KeyValue','Environment'),('VariableName','Site Outdoor Air Drybulb Temperature'),('ReportingFrequency','Hourly')),
              (('KeyValue','Environment'),('VariableName','Site Outdoor Air Dewpoint Temperature'),('ReportingFrequency','Hourly')),
              (('KeyValue','AIR LOOP DEMAND SIDE INLET 1'),('VariableName','System Node Temperature'),('ReportingFrequency','Hourly')),
              ]

VECTOR_SET1 = [
              (('KeyValue','Environment'),('ReportingFrequency','Hourly')),
              ]


#===============================================================================
# Code
#===============================================================================


class ForeignKeysListener(sa.interfaces.PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')

# NOTES
def NOTESONLY_JOINING():
    # This is an easy way to join tables!
    qry = sa.select(['*']).where(tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    # The 'where' method overrides the __eq__ operator to produce an SQL statement
    print(users.c.name == None)

#--- Utilities
def get_metadata(engine):
    metadata = sa.MetaData()
    metadata.reflect(engine)    
    return metadata

def get_engine_from_session(session):
    return session.bind 

#---Query the DB-------------------------


def get_dict(engine, table_object):
    "Given a table object, return all rows of the table as a dictionary"
    column_names = [col.name for col in table_object.c]

    rows = list()

    for row in engine.execute(table_object.select()):
        rows.append(dict(list(zip(column_names,row))))

    return rows




def get_rows(engine,tableObj,maxRows = None):
    """Given a table object, return rows as a list of tuples"""
    s = sa.select([tableObj])
    result = engine.execute(s)

    rows = list()
    idx_row = 1
    for row in result:
        rows.append(row)
        idx_row += 1
        if maxRows and idx_row > maxRows:
            break

    logging.debug("Returned {} rows from {}".format(len(rows),tableObj.name))

    return rows

# def get_table_object(metadata, tableName):
#     """ DOC """
#     return metadata.tables[tableName]

def get_table_object(engine, tableName):
    """ DOC """
    metadata = get_metadata(engine)
    return metadata.tables[tableName]


def get_table_names(engine):
    """ DOC """
    metadata= get_metadata(engine)
    
    return list(metadata.tables.keys())

#def get_table_col_names(engine):
    

def get_number_records(engine,tableObj):
    s = sa.select([sa.func.count(tableObj)])
    return engine.execute(s).fetchone()[0]

#---Update table-------------------------

def insertRows(engine, tableObject, rows):
    """ Uses the transaction design to only commit after transactions ready """
    #logging.info("Inserting {} rows into {}".format(len(rows),tableObject))

    engine.echo = False

    connection = engine.connect()

    #engine
    trans = connection.begin()

    assert not isinstance(rows[0], str)

    for row in rows:
        connection.execute(tableObject.insert().values(row))

    trans.commit()
    engine.echo = False

    logging.info("Inserted {} rows into {}".format(len(rows),tableObject))

#---Pretty print tables-------------------------

def count_rows(engine,tableObj):
    """Just count"""
    s = sa.select([tableObj])
    result = engine.execute(s)

    idx_row = 0
    for row in result:
        idx_row += 1

    return idx_row


def get_pretty_table(engine,tableObj,maxRows = None, verbose = False):
    """Get a PP table given a <sqlalchemy.schema.Table> object
    Return a tuple containing the table name, and the PP rows"""
    columnNames = list(tableObj.columns.keys())
    myTable = PrettyTable(columnNames)

    s = sa.select([tableObj])
    result = engine.execute(s)



    idx_row = 1
    for row in result:
        myTable.add_row(row)
        idx_row += 1
        if maxRows and idx_row > maxRows:
            break
    if verbose:
        logging.info("Created pretty table {}".format(tableObj.name))

    return (tableObj.name, myTable)



def get_all_pretty_tables(engine,maxRows = None):
    """Call get_pretty_table() for all tables in engine"""
    metadata = sa.MetaData()
    metadata.reflect(engine)
    tables = list()
    for table in metadata.sorted_tables:
        tables.append(get_pretty_table(engine, table,maxRows))
    logging.info("Created {} pretty tables".format(len(tables)))

    return tables

def print_all_pretty_tables(engine,maxRows = None):
    """Call get_all_pretty_tables(), and print all to screen"""
    for thisTable in get_all_pretty_tables(engine,maxRows):
        print("***" + thisTable[0] + "***")
        print(thisTable[1])

def printOnePrettyTable(engine, tableName,maxRows = None):
    """Call get_pretty_table(), and print to screen"""
    metadata = sa.MetaData()
    metadata.reflect(engine)
    thisTable = get_table_object(engine, tableName)
    #print thisTable
    #raise
    thisTableData =  get_pretty_table(engine,thisTable,maxRows)
    print("***" + thisTableData[0] + "***")
    print(thisTableData[1])

def sa_join_select():

    s = select([users.c.fullname]).select_from(
                       users.join(addresses,
               addresses.c.email_address.like(users.c.name + '%'))
                                               )

def get_column(table,col_name):
    cols = list()
    for col in table.c:
        cols.append(col)
        #print type(col)
        #print "Name",col.name
        #print col.name,col_name
        if col.name == col_name:
            #print "Yes,"
            return col
    print((col_name, cols))
            
    raise
        



def get_variable_vector(engine, metadata, criteria_list):
    """ Pass in a list of criteria to match, i.e.
    criteria_list = (('KeyValue','3NP:CORR1'),
                        ('VariableName','Zone People Sensible Heating Rate'),
                        ('ReportingFrequency','Monthly'),
                        )
    Possible criteria are taken from the respective tables:
    TimeIndex    ReportVariableDataDictionaryIndex    VariableValue    ReportVariableExtendedDataIndex    TimeIndex    Month    Day    Hour    Minute    Dst    Interval    IntervalType    SimulationDays    DayType    EnvironmentPeriodIndex    WarmupFlag    ReportVariableDataDictionaryIndex    VariableType    IndexGroup    TimestepType    KeyValue    VariableName    ReportingFrequency    ScheduleName    VariableUnits    ReportVariableExtendedDataIndex    MaxValue    MaxMonth    MaxDay    MaxHour    MaxStartMinute    MaxMinute    MinValue    MinMonth    MinDay    MinHour    MinStartMinute    MinMinute

    This function then returns all rows which match these criteria
    Returns the columns from the selection_list
     """
    #===========================================================================
    # Create the query
    #===========================================================================
    # The tables;
    tab_RVdata = get_table_object(metadata, "ReportVariableData")
    tab_time = get_table_object(metadata, "Time")
    tab_RVdata_dictonary = get_table_object(metadata, "ReportVariableDataDictionary")
    tab_RV_extended = get_table_object(metadata, "ReportVariableExtendedData")

    # Join Time and Data
    selection_list = ['Month','Day','Hour','Minute','ReportingFrequency','VariableName','KeyValue','VariableUnits','VariableValue']
    qry = sa.select(selection_list).where(tab_RVdata.c.TimeIndex  == tab_time.c.TimeIndex)

    # Join (Time and Data) with the Dictionary
    qry = qry.where(tab_RVdata.c.ReportVariableDataDictionaryIndex == tab_RVdata_dictonary.c.ReportVariableDataDictionaryIndex)

    #TODO: DO NOT JOIN EXTENDED DATA - It only joins on daily values?
    # Join (Time and Data and Dictionary) with Extended Data
    #qry = qry.where(tab_RVdata.c.ReportVariableExtendedDataIndex == tab_RV_extended.c.ReportVariableExtendedDataIndex)

    #===========================================================================
    # Interim testing
    #===========================================================================
    if 0:
        connection = engine.connect()
        result_iterator = connection.execute(qry)#.fetchall()

        column_headers = list(result_iterator.keys())

        myTable = PrettyTable(column_headers)

        idx_row = 1
        maxRows = 2000
        for row in result_iterator:
            myTable.add_row(row)
            idx_row += 1
            if maxRows and idx_row > maxRows:
                break

        print(myTable)
        raise

    #===========================================================================
    # Build the filter criteria
    #===========================================================================
    for criteria in criteria_list:
        qry = qry.where(get_column(tab_RVdata_dictonary,criteria[0]) == criteria[1])

    tabbed_qry = "\n\t\t".join(qry.__str__().split("\n"))

    logging.debug("Running query \n\t\t{}".format(tabbed_qry))

    #===========================================================================
    # Get the results
    #===========================================================================

    connection = engine.connect()
    results = connection.execute(qry).fetchall()
    print(results)
    raise

    column_headers = list(result_iterator.keys())

    result_vector = list()
    unit = set()
    name = set()
    key = set()

    for row in result_iterator:
        result_vector.append(row['VariableValue'])
        unit.add(row['VariableUnits'])
        name.add(row['VariableName'])
        key.add(row['KeyValue'])

    connection.close()

    assert(len(unit)==1), "Too many columns returned, unit: {}".format(unit)
    assert(len(name)==1), "Too many columns returned, name: {}".format(name)
    assert(len(key)==1), "Too many columns returned, key: {}".format(key)

    result = [[name.pop(),key.pop(),unit.pop()],result_vector]

    logging.info("Returning a vector length {} over {}".format(len(result[1]), result[0]))


    return result



def get_variable_def_from_RVDD(engine, metadata, varName, key_val,interval = "Hourly"):
    logging.info("Selecting {} = {}, {}".format(varName, key_val,interval))

    tReportVariableDataDictionary = get_table_object(metadata, "ReportVariableDataDictionary")
    #s = sa.select([tReportVariableDataDictionary.c.KeyValue])

    #
    #qry = sa.select(["ReportVariableDataDictionaryIndex","VariableUnits"], from_obj=tReportVariableDataDictionary )

    # Get all columns from table
    qry = sa.select(["*"], from_obj=tReportVariableDataDictionary )
    # Match variable name
    qry = qry.where(tReportVariableDataDictionary.c.VariableName == varName)
    # Match key value
    qry = qry.where(tReportVariableDataDictionary.c.KeyValue == key_val)

    # Get results
    results = engine.execute(qry)
    #print qry
    count = 0
    for res in results:
        this_res = res
        count += 1

    assert count == 1

    # Get the column names
    col_names = [c.name for c in tReportVariableDataDictionary.c]

    return dict(list(zip(col_names, this_res)))

def idf_var_names_RVDD(engine, metadata):
    "Gets all variable names from the RVDD"
    tReportVariableDataDictionary = get_table_object(metadata, "ReportVariableDataDictionary")
    #print tReportVariableDataDictionary.columns
    #raise
    s = sa.select([tReportVariableDataDictionary.c.VariableName])

    var_names = ['{}'.format(objName[0]) for objName in engine.execute(s)]

    s = sa.select([tReportVariableDataDictionary.c.KeyValue])

    var_keys = ['{}'.format(objName[0]) for objName in engine.execute(s)]

    return list(zip(var_names,var_keys))

#--- Export

def print_all_excel(engine, path_out, log_type, max_rows = None):
    #max_rows = 1000
    #metadata = get_metadata(engine)
    with log_type:
        writer = pd.ExcelWriter(path_out)
        
        table_names = [table for table in get_table_names(engine)]
        for table_name in table_names:
            fr = get_frame_simple(engine,table_name, max_rows)
            logging.debug("Writing {}, {} rows".format(table_name, len(fr) ))
            fr.to_excel(writer,table_name)
        writer.save()
        logging.critical("Wrote {} tables to {}".format(len(table_names),path_out))
        
def get_frame_simple(engine,table_name,maxRows = None):
    metadata = get_metadata(engine)
    
    tableObj = get_table_object(engine, table_name)
    rows = get_rows(engine,tableObj,maxRows)
    columnNames = list(tableObj.columns.keys())

    # Insert to a dataframe
    if len(rows) == 0:
        df = pd.DataFrame(data=[["EMPTY" for col in columnNames]], columns=columnNames)

    elif len(rows) > 0:
        df = pd.DataFrame(data=rows, columns=columnNames)

    logging.info("Returned a dataframe of shape {}".format(df.shape))

    return df


#--- From EnergyPlus ESO/SQL processing
def get_frame_Eplus(engine):
    metadata = get_metadata(engine)

    """
    ***ReportVariableData***
    +-----------+-----------------------------------+------------------+---------------------------------+
    | TimeIndex | ReportVariableDataDictionaryIndex |  VariableValue   | ReportVariableExtendedDataIndex |
    +-----------+-----------------------------------+------------------+---------------------------------+
    |     1     |                 6                 | -0.0583333333333 |               None              |
    |     1     |                 7                 |      -1.95       |               None              |
    """

    """
    ***Time***
    +-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
    | TimeIndex | Month | Day | Hour | Minute | Dst | Interval | IntervalType | SimulationDays | DayType | EnvironmentPeriodIndex | WarmupFlag |
    +-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
    |     1     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |
    |     2     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |

    """


    """
    ***ReportVariableDataDictionary***
    +-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
    | ReportVariableDataDictionaryIndex | VariableType | IndexGroup | TimestepType |          KeyValue         |             VariableName            | ReportingFrequency | ScheduleName | VariableUnits |
    +-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
    |                 6                 |     Avg      |    Zone    |     Zone     |        Environment        |           Outdoor Dry Bulb          |       Hourly       |     None     |       C       |
    """

    #tab_RVD.TimeIndex = tab_time.TimeIndex
    #tab

    # Join Time and RVD
    tab_RVD = get_table_object(metadata, "ReportVariableData")
    tab_time = get_table_object(metadata, "Time")
    tab_RVDD = get_table_object(metadata, "ReportVariableDataDictionary")
    #qry = sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    #qry = qry.select("VariableValue")
    #qry = qry.select("ReportVariableData"."VariableValue")


    qry = sa.select([tab_RVD.c.VariableValue]).select_from(
                       sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex))



    rvd_time = sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    #ReportVariableDataDictionaryIndex
    # Merge it with the RVDD
    rvd_time_rvdd = sa.join(rvd_time,tab_RVDD,tab_RVD.c.ReportVariableDataDictionaryIndex  == tab_RVDD.c.ReportVariableDataDictionaryIndex)




    #childJoins = childJoins.join(child)

    #print type(qry)
    #qry = qry.select(["VariableValue"])
    #qry = qry.select('"ReportVariableData"."VariableValue"')
    print(rvd_time_rvdd)
    qry = sa.select(["*"]).select_from(rvd_time_rvdd)
    #print qry
    #sa.select()
    #raise
    #qry = qry.where(tab_RVD.c.ReportVariableDataDictionaryIndex == var_idx)
    #print qry
    #print type(qry)
    #print qry.columns

    #qry = qry.where( == var_idx)

    key = "Environment"
    var_name = "Outdoor Dry Bulb"

    qry = qry.where(tab_RVDD.c.VariableName== var_name)
    qry = qry.where(tab_RVDD.c.KeyValue == key)


    #print qry
    #raise
    connection = engine.connect()
    results = connection.execute(qry)
    connection.close()

    print(results)
    print(results.keys)
    #print results["Interval"]
    #raise
    for k in list(results.keys()):
        print(k)
    #for item in dir(results):
    #    print item


    #raise

def get_zone_names(engine,metadata):

    fr_zones = get_frame_simple(engine,metadata,"Zones")

    zone_name_list = fr_zones['ZoneName'].values
    logging.debug("Got {} zone names".format(len(zone_name_list)))

    return zone_name_list


def get_frame_OLD(engine, metadata):
    tab_RVDD = get_table_object(metadata, "ReportVariableDataDictionary")
    #tReportVariableDataDictionary
    qry = sa.select([tab_RVDD])
    qry = qry.where(tab_RVDD.c.ReportingFrequency == "Hourly")
    result = engine.execute(qry)
    for item in result:
        #print type(item)
        this_key = item["KeyValue"]
        this_name = item["VariableName"]
        this_idx = item["ReportVariableDataDictionaryIndex"]
        this_unit = item["VariableUnits"]
        #this_vec = get_variable_vector(engine, metadata, this_idx)
        print(this_key, this_name)

def load_database(fullPath):
    """Given a database path, open it and extract information to create the DesignSpace object

    """
    logging.info("Loading a database from {} ".format(fullPath))

    ECHO_ON = 0
    # Create the connection to the databse
    engine = sa.create_engine('sqlite:///{}'.format(fullPath), echo=ECHO_ON, listeners=[ForeignKeysListener()])
    logging.info("Connected: {} ".format(engine))

    # Create an inspector
    insp = sa.engine.reflection.Inspector.from_engine(engine)
    logging.info("Found tables: {} ".format(", ".join(insp.get_table_names())))

    metadata = sa.MetaData()
    metadata.reflect(bind=engine)

    


def parse_html_to_excel(database_path, output_path):

    engine = sa.create_engine('sqlite:///{}'.format(database_path), echo=ECHO_ON, listeners=[ForeignKeysListener()])
    logging.info("Connected to {} ".format(database_path))

    metadata = sa.MetaData()
    metadata.reflect(engine)

    criteria_list = list()

    zone_name_list = get_zone_names(engine,metadata)

    print(zone_name_list)

    criteria_zone_temp =  [(('KeyValue',zone_name),('VariableName','Zone Mean Air Temperature'),('ReportingFrequency','Hourly')) for zone_name in zone_name_list]
    criteria_list = criteria_list + criteria_zone_temp

    vector_list = list()

    # Get the raw vectors
    for criteria in VECTOR_SET:

        vector = get_variable_vector(engine, metadata,criteria)
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
            dataArray = list(zip(*data)),
            timeArray=None,
            headersArray = list(zip(*headers)),

            headersDef= header_def,
            )
    this_frame = xrg.add_simple_time(this_frame)
    print(this_frame.checkTimeExists())
    xrg.displayFrame(this_frame)

    xl = ExtendedExcelBookAPI(output_path)

    this_frame.saveToExcelAPI(xl,'Comparison')
    xl.save_and_close()
    xl.closeAll()




#        pass
    #print dir(item)
    #print item.items():

    #for k in item:
    #    print k
    #    print dir(item)
#--- Notes
def select_all_from_join(table_a, table_b,engine):
    qry = sa.select(['*'])
    qry = qry.where(table_a.c.individual == table_b.c.hash)
    results = engine.execute(qry)
    rows = results.fetchall()
    
    return rows
    
#--- OLD
def OLD_FROM_SUPER_TABLE():
    raise

    # For testing
    if 0:
        one_row = result_iterator.fetchone()
        for item in zip(column_headers,one_row):
            print(item)

    result = result_iterator.fetchall()


    connection.close()

    logging.info("Matching {} criteria to return {} data rows".format(len(criteria_list), len(result)))
    print(result)
    raise

    result = list(zip(*result))
    result_dict = dict(list(zip(column_headers,result)))
    df = pd.DataFrame(result_dict)

    #===========================================================================
    # Convert to a datetime series
    #===========================================================================


    time_cols = df[['Month','Day','Hour','Minute']]
    new_time_col = list()

    for row in time_cols.values:
        #print row.tolist()
        this_datevec = [2013] + [int(item) for item in row.tolist()]
        #print this_datevec
        this_datevec[3] = this_datevec[3] - 1
        #print this_datevec
        #Y, M,D H,M,S
        new_time_col.append( pd.datetime(*this_datevec) )
    df['datetime'] = new_time_col
    df = df.set_index('datetime')

    df = df.drop(['Month','Day','Hour','Minute'],1)

    logging.info("Created a frame of shape {}".format(df.shape))

    return df



