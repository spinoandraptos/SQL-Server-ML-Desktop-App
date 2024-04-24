'''
The pre-trained ML model and its dependencies are unpacked here and run for data inferencing using real-time data 
fetched from the backend SQL Server. The model prediction is displayed on the frontend GUI as well as stored into the
SQL Server through the backend.

Pre-requisites: a pre-trained ML model packaged using the MLflow Model format
'''
import mlflow
import flask

MODEL_PATH = 'C:/Users/Juncheng/Documents/NUS/CEG/Y2S2/Trane Application Engineer IA/automl_trane_model'

model = mlflow.pyfunc.load_model(MODEL_PATH)
print(type(model))
