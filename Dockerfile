FROM python:2.7-alpine

RUN mkdir -p /app

WORKDIR /app

COPY *.py /app/

CMD python killboard.py
