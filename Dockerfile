FROM python:3-alpine as Base

RUN mkdir -p /usr/src
WORKDIR /usr/src

FROM Base as Installer

RUN \
    apk add --no-cache libffi-dev postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libxslt-dev

COPY requirements.txt /usr/src

RUN pip install -r requirements.txt && \
    apk --purge del .build-deps

FROM Installer as App

ADD ./server /usr/src/server
ADD ./migrations /usr/src/migrations
ADD ./tests /usr/src/tests

COPY pytest.ini /usr/src
COPY wsgi.py /usr/src

# NOTE: Migrations should be built during development

CMD [ "python", "-m", "pytest", "tests/", "--clear-cache" ]