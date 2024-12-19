from lxml import etree

from src.nl_service_metadata_generator.constants import HVD_CATEGORIES_XML


def get_full_nsmap(root):
    nsmap = root.nsmap.copy()
    required_namespaces = {
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gco": "http://www.isotc211.org/2005/gco",
        "gmx": "http://www.isotc211.org/2005/gmx",
        "xlink": "http://www.w3.org/1999/xlink",
        "skos": "http://www.w3.org/2004/02/skos/core#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "euvoc": "http://publications.europa.eu/ontology/euvoc#",
        "bla": "http://purl.org/dc/elements/1.1/",
    }
    nsmap.update({prefix: uri for prefix, uri in required_namespaces.items() if prefix not in nsmap})
    return nsmap


def init_hvd_category_list():

    with open(HVD_CATEGORIES_XML, "r", encoding="utf-8") as file:
        root = etree.XML(file.read().encode("utf-8"))

        nsmap = get_full_nsmap(root)
        categories = [
            {
                "uri": description.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about"),
                "label": pref_label.text.strip(),
                "lang": pref_label.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "").lower(),
                "order": description.find("euvoc:order", namespaces=nsmap).text,
                "id": description.find("bla:identifier", namespaces=nsmap).text
            }
            for description in root.findall(".//rdf:Description", namespaces=nsmap)
            for pref_label in description.findall(".//skos:prefLabel", namespaces=nsmap)
            if pref_label.text and pref_label.attrib.get("{http://www.w3.org/XML/1998/namespace}lang", "").lower() == "nl"
        ]
    return categories


class HVDCategory:

    def __init__(self):
        self.categories = init_hvd_category_list()

    def get_hvd_category_by_id(self, hvd_id: str):
        for category in self.categories:
            if category["id"] == hvd_id:
                return category
        return None

    def get_hvd_category_by_id_list(self, hvd_ids: [str]):
        hvd_categories = []
        for category in self.categories:
            if category["id"] in hvd_ids:
                hvd_categories += [category]
        return hvd_categories
