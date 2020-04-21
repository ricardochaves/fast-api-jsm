FROM python:3.8.2-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
