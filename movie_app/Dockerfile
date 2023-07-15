FROM python:3.12.0b4-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECIDE 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
