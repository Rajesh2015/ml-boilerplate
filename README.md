# React + Flask + PostgreSQL + MLFlow Development Boilerplate

## Overview
Extremely lightweight development environment for a machine-learning prototype application. 

*The intend is to boost your data science dept. so that they can deliver an AI prototype in 3 weeks.*

The app is organized into 4 micro-services:
- [React](https://reactjs.org/) front-end 
- [Flask](http://flask.pocoo.org/) API back-end
- [PostgreSQL](http://postgres.org) SQL database 
- [MLFLow](http://mlflow.org) model engine

The front-end connects to the API by making HTTP requests for desired data.
The API connects to the SQL database and the model engine.
The services are containerized and managed with [Docker Compose](https://docs.docker.com/compose/).

## How to Use
Download [Docker desktop](https://www.docker.com/products/docker-desktop) and follow its
 instructions to install it. This allows us to start using Docker containers.
 
Create a local copy of this repository and run:

    docker-compose build
    
This spins up Compose and builds a local development environment according to 
our specifications in [docker-compose.yml](docker-compose.yml). Keep in mind that 
this file contains settings for *development*, and not *production*.

After the containers have been built (this may take a few minutes), run:

    docker-compose up
    
Test the app by opening this from a browser:

    http://localhost:3000/ 
    
The fruits listed are provided by the API at this endpoint:

    http://localhost:4000/api/v1.0/fruits

In turn, the API issues SQL requests to PostgreSQL at:

    http://localhost:5432

The "Predict" button will request a prediction from the API at this endpoint:

    http://localhost:4000/api/v1.0/predict

In turn, the API will forward the request to the model engine at:

    http://localhost:5000/invocations

## Serving Models with MLFlow
A "Hello World model" has been added to models/model. It will serve all prediction requests by returning "Hello world".

To do something more interesting, download your own model files into models/model and rebuild.

To download a model served by Databricks, run the following function from a notebook:

    %python
    import mlflow
    from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

    def getModel(model_name, model_stage = "Staging", dest_path = "models"):
    local_path = f'file:/databricks/driver/{dest_path}'
    mlflow.set_tracking_uri("databricks")
    
    dbutils.fs.mkdirs(local_path)
    ModelsArtifactRepository(
        f'models:/{model_name}/{model_stage}').download_artifacts("", dst_path = dest_path)

    dbutils.fs.cp("file:/databricks/driver/models/", "/FileStore/{local_path}/", True)
    print(f'{model_stage} Model {model_name} can be downloaded like this:')
    print(f'databricks fs cp dbfs:/FileStore/{dest_path}/ . --recursive --overwrite')
    l = dbutils.fs.ls(f'/FileStore/{dest_path}/')
    return l

You may need to install mlflow on the Databricks cluster:

    %pip install mlflow

After that, you can get the model files by running this:

    cd models/model
    databricks fs cp dbfs:/FileStore/models/ . --recursive --overwrite
    
You may need to install the [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html).

models/model folder should contain files like these (depending on the model):

    conda.yaml
    MLmodel
    python_model.pkl

Once you have replaced the model files, you may have to change the format of the input data.

## Future plans
* Upgrade to latest version of react
* Add boilerplate for running tests locally and through continuous integration.
* Add boilerplate for configuring production-ready settings and deployment.
    * Add AWS RDS for Postgres to terraform cloudops script
        * Make sure local Postgres and RDS Postgres is same version
        * Figure out how to script database initialization
* Expose client and api through HTTPS, set up routing and SSL certs in terraform
* Put together docker-compose.production.yml for AWS AKS
* Create a Jenkins script to build and deploy to AWS AKS

## License
Feel free to use the code in this repository however you wish. Details are provided in
[LICENSE.md](LICENSE.md).


