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



## Keuzes service metadata

- temporalExtent: negeren  element, als dit relevant is dan moet het in de dataset metadata beschreven worden
- securityConstraints: negeren element, als dit relevant is dan moet het in de dataset metadata beschreven worden


## Vragen licentie

- is waarde uit codelist verplicht? https://docs.geostandaarden.nl/md/mdprofiel-iso19119/#codelist-datalicenties
- moet de waarde in het service-metadata record de waarde uit de dataset record overnemen wat betreft de data licenties?
- geldt dit ook voor de uselimitations?
- hoe zit het met licenties met naamsvermelding, moet PDOK daar als service provider de organisatie naam van data provider invullen? of die van pdok... (eerste lijkt me logischer)

## Vragen rol contact

- metadata contact, pdok gebruikt nu waarde pointOfContact > misschien beter resourceProvider (we verstrekken de metadata nl)
- service contact, pdok gebruikt nu waarde author > misschien beter publisher of distributor?

resourceProvider 	Partij die de data verstrekt.
custodian 	Partij verantwoordelijk voor het beheer van de data.
owner 	Partij die eigenaar is van de data.
user 	Partij die de data gebruikt.
distributor 	Partij die de data verstrekt.
originator 	Partij die de data heeft gecreëerd
pointOfContact 	Partij die optreedt als contactpunt voor uitwisselen van kennis of verstrekking van de data.
principalInvestigator 	Partij die betrokken was bij de uitvoering van onderzoek.
processor 	Partij die de data heeft bewerkt, zodanig dat de data is gewijzigd.
publisher 	Partij die de data publiceert.
author 	Partij die auteur is van de data.


## Vragen MD_ClassificationCode 

wel codelijst opgenomen https://docs.geostandaarden.nl/md/mdprofiel-iso19119/#codelist-classificationcode maar nergens gerefereerd, heeft het zin dit element op te nemen in PDOK service metadata?