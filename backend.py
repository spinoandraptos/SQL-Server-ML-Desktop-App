'''
The backend is responsible for data transfer with on-premises SQL Server.

Prerequisites:
1) SQL Server to be connected to the computer running this application over a local network/VPN connection
   such that the SQL Server's local IP address is discoverable by the computer.
2) SQL Server is configured for SQL Server Authentication using username and password.
3) SQL Server allows inbound connections from a specified UDP port.
4) Computer running this application is installed with the same ODBC driver used by the SQL Server

'''
import pyodbc
import os
import pandas as pd
import threading

SERVER = '192.168.1.125'
DATABASE = 'TracerES'
USERNAME = 'sa'
PASSWORD = 'tracerE$'
UDP_PORT = '1433'

PARAM_1_SQL_QUERY = """
SELECT TOP 1 
[DataLogValue],[LastFetchTime]
FROM 
[TracerES].[dbo].[vwTESDataLog_Interval] 
WHERE
DefinitionId = 622
ORDER BY 
LastFetchTime DESC;
"""

PARAM_2_SQL_QUERY = """
SELECT TOP 1 
[DataLogValue]
FROM 
[TracerES].[dbo].[vwTESDataLog_Interval] 
WHERE
DefinitionId = 623
ORDER BY 
LastFetchTime DESC;
"""

PARAM_3_SQL_QUERY = """
SELECT TOP 1 
[DataLogValue]
FROM 
[TracerES].[dbo].[vwTESDataLog_Interval] 
WHERE
DefinitionId = 624
ORDER BY 
LastFetchTime DESC;
"""

PARAM_4_SQL_QUERY = """
SELECT TOP 1
[DataLogValue]
FROM 
[TracerES].[dbo].[vwTESDataLog_Interval] 
WHERE
DefinitionId = 625
ORDER BY 
LastFetchTime DESC;
"""

PARAM_5_SQL_QUERY = """
SELECT TOP 1
[DataLogValue]
FROM 
[TracerES].[dbo].[vwTESDataLog_Interval] 
WHERE
DefinitionId = 626
ORDER BY 
LastFetchTime DESC;
"""

def get_latest_data():

  connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};PORT={UDP_PORT};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD};'
  conn = pyodbc.connect(connectionString) 
  df_1 = pd.read_sql(PARAM_1_SQL_QUERY, conn)
  df_2 = pd.read_sql(PARAM_2_SQL_QUERY, conn)
  df_3 = pd.read_sql(PARAM_3_SQL_QUERY, conn)
  df_4 = pd.read_sql(PARAM_4_SQL_QUERY, conn)
  df_5 = pd.read_sql(PARAM_5_SQL_QUERY, conn)

  curr_time = df_1.loc[0,'LastFetchTime']
  param_1 = df_1.loc[0,'DataLogValue'].astype(float)
  param_2 = df_2.loc[0,'DataLogValue'].astype(float)
  param_3 = df_3.loc[0,'DataLogValue'].astype(float)
  param_4 = df_4.loc[0,'DataLogValue'].astype(float)
  param_5 = df_5.loc[0,'DataLogValue'].astype(float)


def run_function():
    thread = threading.Timer(60.0, run_function) # 60 seconds = 1 minute
    thread.start()
    get_latest_data()

run_function() # start the timer