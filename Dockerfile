FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    locales \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8     

COPY . /ngr-md-generator-src
RUN pip3 install /ngr-md-generator-src
ENV PATH="/usr/local/bin"
ENTRYPOINT [ "generate-metadata" ]
