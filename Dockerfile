FROM python:3.12
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    cron \
    sqlite3

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

