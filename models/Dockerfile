FROM continuumio/miniconda3

RUN apt-get update && apt-get install
RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

ENV MLFLOW_HOME /opt/mlflow
ENV MLFLOW_VERSION 1.17.0
ENV MLFLOW_PORT 5000

RUN conda install -c conda-forge bash
RUN conda install -c conda-forge mlflow=${MLFLOW_VERSION}

COPY model/ ${MLFLOW_HOME}/model

WORKDIR ${MLFLOW_HOME}

RUN mlflow models prepare-env -m ${MLFLOW_HOME}/model

RUN useradd -d ${MLFLOW_HOME} mlflow
RUN chown -hR mlflow: ${MLFLOW_HOME}
RUN chown -hR mlflow: /opt/conda/envs/
USER mlflow

CMD mlflow models serve -m ${MLFLOW_HOME}/model --host 0.0.0.0 --port ${MLFLOW_PORT}