FROM python:3.8.2-buster

WORKDIR /web

COPY . /web

RUN pip install -r requirements.txt
