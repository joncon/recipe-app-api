FROM python:3.7-alpine
MAINTAINER Me

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-libs
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# RUN apk del .tmp-build-deps
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D creates user for application process only no home dir
RUN adduser -D user
#Switch to user
USER user
