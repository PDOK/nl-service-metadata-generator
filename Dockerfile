FROM python:3.10.8-slim-bullseye
LABEL maintainer="Anton Bakker <anton.bakker@kadaster.nl>"
COPY . /src


RUN pip install --upgrade setuptools && \
    pip install /src

ENTRYPOINT [ "nl-service-metadata-generator" ]
