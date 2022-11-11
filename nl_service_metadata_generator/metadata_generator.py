import json
from datetime import datetime

from nl_service_metadata_generator.codelist_lookup import (
    get_inspire_fields_by_ogc_service_type,
    get_inspire_theme_label,
    get_sds_categories,
    get_service_protocol_values,
    get_spatial_dataservice_categories,
)
from nl_service_metadata_generator.constants import (
    JSON_SCHEMA_CONTACT,
    JSON_SCHEMA_SERVICE,
    SERVICE_TEMPLATE,
)
from nl_service_metadata_generator.util import (
    camel_to_snake,
    format_xml,
    get_service_md_identifier,
    get_service_url,
    render_template,
    replace_keys,
    validate_input_json,
)


def add_dynamic_fields(data_json, ogc_service_type):
    md_date_stamp = datetime.today().strftime("%Y-%m-%d")
    title = data_json["service_title"]
    if not title.lower().endswith(ogc_service_type.lower()):
        data_json["service_title"] = f"{title} {ogc_service_type}"
    data_json["md_date_stamp"] = md_date_stamp

    if (
        not "service_revision_date" in data_json
        or not data_json["service_revision_date"]
    ):
        data_json["service_revision_date"] = md_date_stamp
    data_json["service_type"] = ogc_service_type
    protocol_fields = get_service_protocol_values(ogc_service_type)
    data_json.update(protocol_fields)
    service_access_point = get_service_url(data_json, ogc_service_type)
    data_json["service_access_point"] = service_access_point

    service_md_identifier = get_service_md_identifier(data_json, ogc_service_type)
    data_json["md_identifier"] = service_md_identifier

    # remove keywords that are equal to spatial_dataservice_category_label (
    # these kw are already taken care of by get_inspire_fields_by_ogc_service_type
    categories = get_spatial_dataservice_categories()
    kw_to_delete = [kw for kw in data_json["keywords"] if kw in categories]
    for kw in kw_to_delete:
        data_json["keywords"].remove(kw)
    # enfore lowercase keywords
    data_json["keywords"] = [kw.lower() for kw in data_json["keywords"]]
    # some inspire related fields are also mandatory in the "vanilla" NL profiel
    inspire_fields = get_inspire_fields_by_ogc_service_type(ogc_service_type)
    data_json.update(inspire_fields)

    if data_json["inspire_type"] == "other":
        data_json["inspire_servicetype"] = "other"
        sds_values = get_sds_categories(
            data_json["sds_category"]
        )  # by default all other services are invokable services, see discussion here: https://github.com/INSPIRE-MIF/helpdesk/issues/25
        data_json["sds_category_uri"] = sds_values["uri"]
        data_json["sds_category"] = str(data_json["sds_category"].value)
    inspire_theme_label = get_inspire_theme_label(data_json)
    if inspire_theme_label:
        data_json["inspire_theme_label"] = inspire_theme_label
    return data_json


def generate_service_metadata(
    contact_config_file,
    metadata_config_file,
    service_type,
    inspire_type,
    sds_type,
    csw_endpoint,
):
    with open(metadata_config_file, "r") as md_config_file, open(
        contact_config_file, "r"
    ) as contact_config_file:
        md_config = json.loads(md_config_file.read())
        contact_config = json.loads(contact_config_file.read())

        validate_input_json(contact_config, JSON_SCHEMA_CONTACT)
        validate_input_json(md_config, JSON_SCHEMA_SERVICE)

        contact_config = replace_keys(contact_config, camel_to_snake)
        md_config = replace_keys(md_config, camel_to_snake)
        md_config.update(contact_config)

        # add variables supplied by args
        md_config["inspire_type"] = inspire_type
        md_config["sds_category"] = sds_type
        md_config["csw_endpoint"] = csw_endpoint

        # add dynamic fields from lookup table
        md_config = add_dynamic_fields(md_config, service_type)
        md_record = render_template(SERVICE_TEMPLATE, md_config)
        return format_xml(md_record)
