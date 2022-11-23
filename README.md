# nl-service-metadata-generator

[![PyPI version](https://badge.fury.io/py/nl-service-metadata-generator.svg)](https://pypi.org/project/nl-service-metadata-generator/)

CLI applicatie om service metadata records te genereren die voldoen aan het [Nederlands profiel op ISO 19119 voor services versie 2.1.0](https://docs.geostandaarden.nl/md/mdprofiel-iso19119/).

CLI applicatie genereert metadata en voert schema validatie uit. Applicatie voert _geen_ schematron validatie uit (validatie op _Nederlands profiel op ISO 19119 voor services versie 2.1.0_).

## Service Types

De nl-service-metadata-generator ondersteunt de volgende service types:

- geen INSPIRE service
- INSPIRE network service
- INSPIRE other service
  - Spatial Data Service (SDS) - invocable
  - SDS - interoperable

> N.B. SDS harmonized wordt dus niet ondersteund door de nl-service-metadata-generator

## Installation

Installeer `nl-service-metadata-generator` als pip package (uitvoeren vanuit root van repository):

```pip3
pip3 install .
```

Nu moet het cli command `nl-service-metadata-generator` beschikbaar zijn in `PATH`.

## Usage

```bash
Usage: nl-service-metadata-generator generate
           [OPTIONS] {csw|wms|wmts|wfs|wcs|sos|atom|tms|oaf}
           {network|other|none} CONSTANTS_CONFIG_FILE METADATA_CONFIG_FILE
           OUTPUT_FILE

Options:
  --csw-endpoint TEXT             References to dataset metadata records will
                                  use this CSW endpoint (default val: https://
                                  nationaalgeoregister.nl/geonetwork/srv/dut/c
                                  sw)
  --sds-type [invocable|interoperable]
                                  only applies when inspire-type='other'
  --help                          Show this message and exit.
```

Bijvoorbeeld (uitvoeren in root directory van dit repository):

```bash
nl-service-metadata-generator atom network example_json/contact.json example_json/inspire.json atom.xml
```

JSON schema voor de `CONSTANTS_CONFIG_FILE` en `METADATA_CONFIG_FILE` kunnen worden opgevraagd middels het `show-schema` command, zie `nl-service-metadata-generator show-schema --help` voor help.

## Development

Voor het formatteren van code installeer [`black`](https://pypi.org/project/black/) en draai vanuit de root van het repo:

```sh
black .
```

Verwijderen van ongebruikte imports met [`autoflake`](https://pypi.org/project/autoflake/):

```sh
autoflake --remove-all-unused-imports -i -r .
```

Organiseren en orderen imports met [`isort`](https://pypi.org/project/isort/):

```sh
isort  -m 3 .
```

## Docker

Bouw docker image met:

```sh
docker build . -t nl-service-metadata-generator
```

Dan container starten met (n.b. `-u root` argument, is nodig voor priviliges Docker container om bestanden weg te schrijven in folder mount - niet op deze manier gebruiken voor productie doeleinden):

```sh
docker run --user root -v /home/anton/workspace/github.com/PDOK/nl-service-metadata-generator/example_json:/data nl-service-metadata-generator generate atom network /data/constants.json /data/inspire.json /data/atom.xml
```
