FROM python:3.6-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN apk update && apk add bash
RUN apk add --no-cache bash
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN pip3 install -r requirements.txt
COPY . /usr/src/app
ENV FLASK_APP app.py

EXPOSE 5000
CMD ["/bin/bash", "./boot.sh"]
