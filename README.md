# nl-service-metadata-generator

CLI applicatie om service metadata records te genereren die voldoen aan het [Nederlands profiel op ISO 19119 voor services versie 2.1.0](https://docs.geostandaarden.nl/md/mdprofiel-iso19119/).

CLI applicatie genereert metadata en voert schema validatie uit. Applicatie voert *geen* schematron validatie uit (validatie op *Nederlands profiel op ISO 19119 voor services versie 2.1.0*).

## Installation

Installeer `nl-service-metadata-generator` als pip package (uitvoeren vanuit root van repository):

```pip3
pip3 install .
```

Nu moet het cli command `nl-service-metadata-generator` beschikbaar zijn in `PATH`.

## Usage

```bash
Usage: nl-service-metadata-generator [OPTIONS]
                                     {csw|wms|wmts|wfs|wcs|sos|atom|tms|oaf}
                                     {network|other|none} CONTACT_CONFIG_FILE
                                     METADATA_CONFIG_FILE OUTPUT_FILE

Options:
  --csw-endpoint TEXT             References to dataset metadata records will
                                  use this CSW endpoint (default val: https://
                                  nationaalgeoregister.nl/geonetwork/srv/dut/c
                                  sw)
  --sds-type [invocable|interoperable|harmonised]
                                  only applies when inspire-type='other'
  --help                          Show this message and exit.
```

Bijvoorbeeld (uitvoeren in root directory van dit repository):

```bash
nl-service-metadata-generator atom network example_json/contact.json example_json/inspire.json atom.xml
```
