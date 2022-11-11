FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \ 
    python3.10-venv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /src

RUN pip install --upgrade setuptools && \
    pip install /src

ENTRYPOINT [ "nl-service-metadata-generator" ]
