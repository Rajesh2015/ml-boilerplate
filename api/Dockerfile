FROM python:3.7
RUN mkdir /backend
WORKDIR /backend
ADD . /backend
COPY requirements.txt /backend/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt