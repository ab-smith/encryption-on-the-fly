FROM python:alpine3.10
MAINTAINER Abderrahmane SMIMITE

RUN apk add build-base openssl-dev libffi-dev vim py-gunicorn

RUN mkdir /app
COPY requirements.txt /app
COPY app.py /app
COPY wsgi.py /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["./start.sh"]