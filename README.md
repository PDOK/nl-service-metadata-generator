# NGR Metadata Generator

CLI applicatie om service metadata records te genereren die voldoen aan het [Nederlands profiel op ISO 19119 voor services versie 2.0.0](https://docs.geostandaarden.nl/md/mdprofiel-iso19119/).

CLI applicatie genereert metadata en voert schema validatie uit. Applicatie voert *geen* schematron validatie uit (validatie op *Nederlands profiel op ISO 19119 voor services versie 2.0.0*). 

## Gebruik

Installeer eerst de dependencies (getest op Ubuntu in Bash shell):

```
pip3 install -r requirements.txt
```

Voor help:

```
./generate_md.py --help
Usage: generate_md.py [OPTIONS] VALUES_JSON_PATH
                      [CSW|WMS|WMTS|WFS|WCS|SOS|ATOM]

  Generate metadata record.

Options:
  --output-dir PATH
  --help             Show this message and exit.
```

Bijvoorbeeld (uitvoeren in root directory van dit repository):

```
mkdir output && ./generate_md.py example_json/protectedsites_cdda_harmonized.json WMS --output-dir output/
```
