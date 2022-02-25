FROM python:3.9

WORKDIR /ml-boilerplate/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /ml-boilerplate/api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /ml-boilerplate/api

WORKDIR /ml-boilerplate