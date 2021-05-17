FROM python:3.9-slim

LABEL maintainer="Meryll Dindin meryll@calaster.com"

RUN mkdir /app
VOLUME /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD [ "gunicorn", "-w 1", "-t 240", "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "main:app" ]
