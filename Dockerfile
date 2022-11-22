FROM python:3.10.8-slim-bullseye

COPY . /src

RUN pip install --upgrade setuptools && \
    pip install /src

RUN groupadd -r cli-user && useradd -r -s /bin/false -g cli-user cli-user
USER cli-user

ENTRYPOINT [ "nl-service-metadata-generator" ]
