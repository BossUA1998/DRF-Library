FROM python:3.13-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /drf-library

COPY requirements.txt /drf-library/
RUN python -m pip install -r requirements.txt

COPY . /drf-library/

RUN adduser -D docker_user
USER docker_user
