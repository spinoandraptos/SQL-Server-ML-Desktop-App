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
import urllib.request
import json
import os
import ssl
import pandas as pd
import threading

SERVER = '192.168.1.125'
DATABASE = 'TracerES'
USERNAME = 'sa'
PASSWORD = 'tracerE$'
UDP_PORT = '1433'
ML_ENDPOINT = 'https://trane-ml-nijct.southeastasia.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
API_KEY = 'jnDmwRxpcYpcfHfRqBMAe3dSu43SNcnP'
CSV_LOG = './ML_log_updated.csv'

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

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def get_ML_prediction():

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

  allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

  data =  {
    "input_data": {
      "columns": [
        "CurrTime5Value",
        "CurrTime4Value",
        "CurrTime2Value",
        "CurrTime1Value"
      ],
      "index": [1],
      "data": [[param_5, param_4, param_2, param_1]]
    }
  }

  body = str.encode(json.dumps(data))

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ API_KEY), 'azureml-model-deployment': 'automl-trane-model-1' }
  req = urllib.request.Request(ML_ENDPOINT, body, headers)

  try:
      response = urllib.request.urlopen(req)
      result = response.read().decode()
      result = result.strip("[").strip("]")

      df = pd.read_csv(CSV_LOG)
      if df.empty:
        new_row = pd.DataFrame([[curr_time, result, 0]],columns=['Time','ML Endpoint Predicted Future', 'Actual Future Value'])
        df = pd.concat([df,new_row], ignore_index = True)
      else:
        curr_last_index = df.iloc[-1].name
        new_row = pd.DataFrame([[curr_time, result, 0]],columns=['Time','ML Endpoint Predicted Future', 'Actual Future Value'])
        df = pd.concat([df,new_row], ignore_index = True)
        df["Actual Future Value"][curr_last_index] = param_3
      df = df.reset_index(drop=True)
      df.to_csv(CSV_LOG, index=False)

  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))
      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))

def run_function():
    thread = threading.Timer(60.0, run_function) # 60 seconds = 1 minute
    thread.start()
    get_ML_prediction()

run_function() # start the timer