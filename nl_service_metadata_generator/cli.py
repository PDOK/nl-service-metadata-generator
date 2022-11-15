#!/usr/bin/env python3
import os
from pathlib import Path

import click

from nl_service_metadata_generator.constants import DEFAULT_CSW_ENDPOINT
from nl_service_metadata_generator.enums import (
    InspireType,
    SchemaType,
    SdsType,
    ServiceType,
)
from nl_service_metadata_generator.metadata_generator import generate_service_metadata
from nl_service_metadata_generator.util import print_schema, validate_service_metadata


@click.group()
def cli():
    pass


@cli.command(name="inspect-schema")
@click.argument("schema-type", type=click.Choice(SchemaType, case_sensitive=True))
def inspect_schema_command(schema_type):
    print_schema(schema_type)


@cli.command(name="generate")
@click.argument("service-type", type=click.Choice(ServiceType, case_sensitive=True))
@click.argument("inspire-type", type=click.Choice(InspireType, case_sensitive=True))
@click.argument("contact-config-file", type=click.Path(exists=True))
@click.argument("metadata-config-file", type=click.Path(exists=True))
@click.argument("output-file", type=click.Path(exists=False))
@click.option(
    "--csw-endpoint",
    type=str,
    default=DEFAULT_CSW_ENDPOINT,
    help=f"References to dataset metadata records will use this CSW endpoint (default val: {DEFAULT_CSW_ENDPOINT})",
)
@click.option(
    "--sds-type",
    type=click.Choice(SdsType, case_sensitive=True),
    default=SdsType.INVOCABLE,
    help="only applies when inspire-type='other'",
)
def generate_command(
    service_type: ServiceType,
    inspire_type: InspireType,
    contact_config_file,
    metadata_config_file,
    output_file,
    csw_endpoint,
    sds_type: SdsType,
):
    if sds_type == SdsType.HARMONISED:
        raise NotImplementedError(
            "Spatial Data Service (SDS) type 'harmonised' not implemented yet."
        )

    md_record = generate_service_metadata(
        contact_config_file,
        metadata_config_file,
        service_type,
        inspire_type,
        sds_type,
        csw_endpoint,
    )
    validation_result = validate_service_metadata(md_record)

    if validation_result:
        print(
            f"metadata-generator error: generated metadata is invalid, validation message: {validation_result}"
        )
    if output_file != "-":
        output_dir = os.path.dirname(output_file)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        if validation_result:
            output_file = f"{output_file}.invalid"

        with open(output_file, "w") as output:
            output.write(md_record)
    else:
        if validation_result:
            exit(1)
        print(md_record)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
