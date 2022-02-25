FROM continuumio/miniconda3

ENV MLFLOW_HOME /opt/mlflow
ENV MLFLOW_PORT 5000

RUN conda install -c conda-forge bash
RUN conda install -c conda-forge mlflow

COPY model/ ${MLFLOW_HOME}/model

WORKDIR ${MLFLOW_HOME}

RUN useradd -d ${MLFLOW_HOME} mlflow
RUN chown -hR mlflow: ${MLFLOW_HOME}
RUN chown -hR mlflow: /opt/conda/envs/
USER mlflow

RUN mlflow models prepare-env -m ${MLFLOW_HOME}/model

CMD mlflow models serve -m ${MLFLOW_HOME}/model --host 0.0.0.0 --port ${MLFLOW_PORT}