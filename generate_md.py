#!/usr/bin/env python3

import glob
import os
import json
from datetime import datetime
import click
from lxml import etree
import pystache

SERVICE_TEMPLATES = {
    "harmonized":"templates/iso19119_nl_profile_2.0_template_inspire_harmonized.mustache",
    "none":"templates/iso19119_nl_profile_2.0_regular.mustache",
}

CODELIST_JSON_FILE = "json/codelists.json"

def get_inspire_theme_label(data_json):
    inspire_mode = data_json["inspire"]
    if inspire_mode != "none":
        with open(CODELIST_JSON_FILE, 'r') as json_file:
            codelists_json = json.loads(json_file.read())
            inspire_themes_codelist = codelists_json['inspire_themes']
            inspire_theme_uri = data_json['inspire_theme_uri']
            if inspire_theme_uri not in inspire_themes_codelist:
                raise Exception(f"inspire theme uri {inspire_theme_uri} unknown. See https://www.eionet.europa.eu/gemet/nl/inspire-themes/ for supported values.")
            return inspire_themes_codelist[inspire_theme_uri]
    return ""

def get_inspire_fields_by_service_protocol(service_protocol):
    # "inspire_service_type": "view",
    with open(CODELIST_JSON_FILE, 'r') as json_file:
        codelists_json = json.loads(json_file.read())
        inspire_servicetypes_codelist = codelists_json["codelist_inspire_service_types"]
        for item in inspire_servicetypes_codelist:
            if service_protocol in item["protocols"]:
                item.pop("protocols")
                return item

def get_service_protocol_values(service_type):
    # "service_protocol_name": "OGC:WMS",
    # "service_protocol_url": "http://www.opengeospatial.org/standards/wms"
    with open(CODELIST_JSON_FILE, 'r') as json_file:
        codelists_json = json.loads(json_file.read())
        inspire_servicetypes_codelist = codelists_json["codelist_protocol"]
        return inspire_servicetypes_codelist[service_type]

def get_service_template(data_json):
    inspire_mode = data_json["inspire"]
    if inspire_mode not in SERVICE_TEMPLATES:
        keys_string = ", ".join(SERVICE_TEMPLATES.keys())
        raise Exception(f"inspire mode {inspire_mode} not supported. Supported values: {keys_string}")
    result = SERVICE_TEMPLATES[inspire_mode]
    return result

def get_service_url(data_json, service_type):
    # for now do not generate urls dynamically but use fallback 
    # based on key service_capabilities_url_<service_type>
    service_type_string = service_type.lower().replace(" ", "_")
    key = f"service_capabilities_url_{service_type_string}"
    if not key in data_json:
        raise Exception(f"key {key} missing in values-json input")
    return data_json[key]

def add_dynamic_fields(data_json, service_type):
    md_date_stamp = datetime.today().strftime('%Y-%m-%d')
    title = data_json["service_title"]
    data_json["service_title"] = f"{title} {service_type}"
    data_json["md_date_stamp"] = md_date_stamp
    data_json["service_revision_date"] = md_date_stamp
    data_json["service_type"] = service_type
    protocol_fields = get_service_protocol_values(service_type)
    data_json.update(protocol_fields)
    service_protocol = data_json["service_protocol"]
    inspire_fields = get_inspire_fields_by_service_protocol(service_protocol)
    data_json.update(inspire_fields)
    service_capabilities_url = get_service_url(data_json, service_type)
    data_json["service_capabilities_url"] = service_capabilities_url
    inspire_theme_label = get_inspire_theme_label(data_json)
    if inspire_theme_label:
        data_json["inspire_theme_label"] = inspire_theme_label
    # print(json.dumps(data_json))
    return data_json

def render_template(template_path, data_json, partials_path=""):
    result = ""
    with open(template_path, 'r') as template_file:
        template_string = template_file.read()
    partials = {}
    if partials_path:
        for partial_file in glob.glob(os.path.join(partials_path, "*.mustache")):
            basename = os.path.splitext(os.path.basename(partial_file))[0]
            with open(partial_file, "r") as partial_template:
                p_string = partial_template.read()
            partials[basename] = p_string
    renderer = pystache.Renderer(partials=partials)
    result = renderer.render(template_string, data_json)
    return result

def get_md_identifier(json_path):
     with open(json_path, 'r') as json_file:
        config_json = json.loads(json_file.read())
        return config_json["md_identifier"]

def generate_service_metadata(json_path, service_type):
    with open(json_path, 'r') as json_file:
        config_json = json.loads(json_file.read())
        service_template = get_service_template(config_json)
        config_json = add_dynamic_fields(config_json, service_type)
        md_record = render_template(service_template, config_json, "templates/partials")
        validation_result = validate_service_metadata(md_record)
        if validation_result:
            print(f"metadata-generator error: generated metadata is invalid, validation message: {validation_result}")
            exit(1)
        parser = etree.XMLParser(remove_comments=True, remove_blank_text=True)
        tree = etree.fromstring(md_record.encode('utf-8'), parser=parser)
        return etree.tostring(tree, pretty_print=True).decode('utf-8')

def validate_xml_form(xml_string):
    result = ""
    try:
        parser = etree.XMLParser()
        etree.fromstring(xml_string.encode('utf-8'), parser=parser)
    except IOError:
        result = "Invalid File"
    # check for XML syntax errors
    except etree.XMLSyntaxError as err:
        result = "XML Syntax Error: {0}".format(err.msg)
    return result

def validate_service_metadata(xml_string):
    result = validate_xml_form(xml_string)
    if result:
        return result
    schema_path = "schema/gmd_gmx.xsd"
    with open(schema_path, 'rb') as xml_schema_file:
        schema_doc = etree.XML(xml_schema_file.read(), base_url=schema_path)
        schema = etree.XMLSchema(schema_doc)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        xml_string = etree.XML(xml_string.encode('utf-8'), parser=parser)
        if not schema.validate(xml_string):
            for error in schema.error_log:
                result += f"\n\terror: {error.message}, line: {error.line}, column {error.column}"
    return result

@click.group()
def cli():
    pass

@cli.command(name="gen-md")
@click.argument('values-json-path', type=click.Path(exists=True))
@click.argument('service-type', type=click.Choice(\
    ['CSW', 'WMS', 'WMTS', 'WFS', 'WCS', 'SOS', 'ATOM'], case_sensitive=False))
@click.option('--output-dir', type=click.Path(exists=False), help="")
def generate_service_metadata_command(values_json_path, service_type, output_dir=""):
    """Generate metadata record.
    """
    md_record = generate_service_metadata(values_json_path, service_type)
    md_identifier = get_md_identifier(values_json_path)
    if output_dir:
        output_filename = f"{output_dir}/{md_identifier}_{service_type}.xml"
        with open(output_filename, 'w') as output:
            output.write(md_record)
    else:
        print(md_record)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    generate_service_metadata_command()
