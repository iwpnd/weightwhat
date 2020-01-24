FROM python:3.7.5-alpine

WORKDIR /usr/src/weightwhat

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/weightwhat/requirements.txt

# dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/weightwhat/requirements.txt \
    && rm -rf /root/.cache/pip

COPY ./src /usr/src/weightwhat
