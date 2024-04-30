# SQL-Server-MLflow-Desktop-App
A python-based Windows desktop application to perform real-time machine learning predictions based on on-premises SQL Server data using a pre-trained MLflow model. This application is suitable for integration with Azure Machine Learning workflows where a registered supervised learning MLflow model is to be deployed locally instead of as an online endpoint. The application supports customisation of data sources and sinks, making it a versatile tool for working with a variety of MLflow models.

## Features:
- ### Custom MLflow Model Selection

    - Simply save your MLflow model in a local directory and locate the model directory in the application to use it. 
    - Required files in the model directory: MLmodel file, model.pkl, requirements.txt, python_env.yaml, conda.yaml
    - Most supervised learning MLflow models are supported by this application. 

- ### Data Visualisation 
