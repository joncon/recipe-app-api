FROM python:3.7-alpine
MAINTAINER Me

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D creates user for application process only no home dir
RUN adduser -D user
#Switch to user
USER user
