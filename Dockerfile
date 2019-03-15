FROM python:3.7-alpine
MAINTAINER Me

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache postgresql-libs jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D creates user for application process only no home dir
#media is for uploads
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 775 /vol/web
#Switch to user
USER user
