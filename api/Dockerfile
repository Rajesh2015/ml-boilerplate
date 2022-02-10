FROM python:3.8.3-slim

RUN apt-get update && apt-get install
RUN apt-get install -y \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN python -m pip install --upgrade pip

# set work directory
WORKDIR /ml-boilerplate/api

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY requirements.txt /ml-boilerplate/api/requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# copy project
# COPY src /usr/app/src/
COPY . /ml-boilerplate/api

# set work directory
WORKDIR /ml-boilerplate