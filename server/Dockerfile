# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster

FROM python:3.8-slim

LABEL maintainer="Meryll Dindin meryll@calaster.com"

RUN mkdir /app
VOLUME /app
WORKDIR /app
RUN pip install pip --upgrade
RUN pip install gunicorn uvicorn==0.11.8
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000

CMD [ "gunicorn", "-w 3", "-t 240", "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "main:app" ]