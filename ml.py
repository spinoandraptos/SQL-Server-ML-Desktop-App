'''
The pre-trained ML model and its dependencies are unpacked here and run for data inferencing using real-time data 
fetched from the backend SQL Server. The model prediction is displayed on the frontend GUI as well as stored into the
SQL Server through the backend.

Pre-requisites: a pre-trained ML model packaged using the MLflow Model format
'''
import pandas as pd
import numpy as np
import mlflow
import subprocess
'''
Inputs are based on the model signature found in MLmodel file
Provide a dict of param-value pairs, taking note of data type required and name of each parameter
'''
# inputs = {"CurrTime5Value": np.float32(1.0), "CurrTime4Value": np.float32(2.0), "CurrTime2Value": np.float32(3.0), "CurrTime1Value": np.float32(4.0)}
'''
Runs the shell command to install all necessary requirements needed by the packaged model before proceeding
'''
# dependecies_path = mlflow.pyfunc.get_model_dependencies(MODEL_PATH, format='pip')
# subprocess.run([f"pip install -r '{MODEL_PATH}/requirements.txt'"], shell=True)

def runMlPrediction(MODEL_PATH, inputs):
    model = mlflow.pyfunc.load_model(MODEL_PATH)
    predictions = model.predict(inputs)
    print(predictions)
