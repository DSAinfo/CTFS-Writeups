FROM python:3.6.6-alpine3.8

ENV FLASK_APP /www/app.py
ENV FLASK_DEBUG 1
ENV FLASK_RUN_PORT 8888

RUN apk add bash gcc musl-dev mysql mariadb-dev build-base

ADD entrypoint.sh /entrypoint.sh

RUN mkdir /www

EXPOSE 8888

ENTRYPOINT [ "/entrypoint.sh" ]
