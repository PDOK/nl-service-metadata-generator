# NGR Metadata Generator

CLI applicatie om service metadata records te genereren die voldoen aan het [Nederlands profiel op ISO 19119 voor services versie 2.0.0](https://docs.geostandaarden.nl/md/mdprofiel-iso19119/).

CLI applicatie genereert metadata en voert schema validatie uit. Applicatie voert *geen* schematron validatie uit (validatie op *Nederlands profiel op ISO 19119 voor services versie 2.0.0*).

## Benodigdheden (Ubuntu 20 LTS)

Installeer python3

```
sudo snap install python3
```

Installeer de python3 package installer (pip3)

```
sudo apt install python3-pip
```

Installeer libxml-dev

```
sudo apt install libxml2-dev
```

Installeer libxslt-dev
```
sudo apt install libxslt-dev
```

## Gebruik

Installeer ngr-metadata-generator als pip package (uitvoeren vanuit root van repository):

```pip3
pip3 install .
```

Nu moet het cli command `generate-metadata`/`gen-md` beschikbaar zijn in `PATH`. Mocht dit niet het geval zijn, kijk of de binary goed is geïnstalleerd in `$HOME/.local/bin/gen-md` en voeg deze vervolgens toe aan je `PATH`

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Dit is de output van `generate-metadata`/`gen-md`:

```bash
generate-metadata --help
Usage: generate-metadata [OPTIONS] VALUES_JSON_PATH
                         [CSW|WMS|WMTS|WFS|WCS|SOS|ATOM] [PROD|TEST]

  Generate metadata record.

Options:
  --output-dir PATH
  --help             Show this message and exit.
```

Bijvoorbeeld (uitvoeren in root directory van dit repository):

```bash
gen-md example_json/inspire.json WMS PROD --output-dir output/
```
