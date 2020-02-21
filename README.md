# NGR Metadata Generator

CLI applicatie om service metadata records te genereren die voldoen aan het [Nederlands profiel op ISO 19119 voor services versie 2.0.0](https://docs.geostandaarden.nl/md/mdprofiel-iso19119/).

CLI applicatie genereert metadata voert zowel JSON Schema validatie uit op de input JSON als een XSD schema validatie op de XML output. Applicatie voert *geen* schematron validatie uit (validatie op *Nederlands profiel op ISO 19119 voor services versie 2.0.0*). 

## Gebruik

Installeer ngr-metadata-generator als pip package (uitvoeren vanuit root van repository):

```
pip3 install .
```

Nu moet het cli command `generate-metadata`/`gen-md` beschikbaar zijn het `PATH`:

```
generate-metadata --help
Usage: generate-metadata [OPTIONS] VALUES_JSON_PATH
              [CSW|WMS|WMTS|WFS|WCS|SOS|ATOM|TMS|IN_JSON] [PROD|TEST]
              OUTPUT_FILE

  Generate metadata record.

Options:
  --help  Show this message and exit.
```

Bijvoorbeeld (uitvoeren in root directory van dit repository):

```
gen-md example_json/protectedsites_cdda_harmonized.json WMS PROD output/protectedsites_cdda_harmonized.xml
```
