FROM python:3.8.5-alpine

WORKDIR /app
COPY requirements.txt .
ENV PYTHON_ENV docker

RUN apk update && \
apk add postgresql-dev gcc python3-dev musl-dev g++ && \
apk add git && \
apk add --no-cache --upgrade bash && \
pip install -r requirements.txt

COPY . /app

EXPOSE 5432  22 443 9418 6379