FROM python:alpine3.10
MAINTAINER Abderrahmane SMIMITE

RUN apk add build-base openssl-dev libffi-dev vim
RUN pip install cffi cryptography flask

RUN mkdir /app
COPY app.py /app
WORKDIR /app

EXPOSE 5000

CMD ["python3", "app.py"]