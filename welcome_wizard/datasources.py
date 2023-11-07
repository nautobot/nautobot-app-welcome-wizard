"""Datasources for Welcome Wizard."""

import os
from pathlib import Path

import yaml
from nautobot.extras.choices import LogLevelChoices
from nautobot.extras.registry import DatasourceContent

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


def retrieve_device_types_from_filesystem(path):
    """Retrieve Manufacturers and Device Types from the file system.

    Args:
        path (str): Filesystem path to the repo holding the Device Types.

    Returns:
        tuple: a Set of Manufacturers and a dictionary of Device Types.
    """
    manufacturers = set()
    device_types = {}

    device_type_path = os.path.join(path, "device-types")
    files = (filename for filename in Path(device_type_path).rglob("*") if filename.suffix in [".yml", ".yaml"])
    for filename in files:
        with open(filename, encoding="utf8") as file:
            data = yaml.safe_load(file)

        manufacturers.add(data["manufacturer"])
        device_types[filename.name] = data
    return (manufacturers, device_types)


def refresh_git_import_wizard(repository_record, job_result, delete=False):
    """Callback for GitRepository updates - refresh Device Types managed by it."""
    if "welcome_wizard.import_wizard" not in repository_record.provided_contents or delete:
        # TODO Handle delete.
        return

    manufacturers, device_types = retrieve_device_types_from_filesystem(repository_record.filesystem_path)
    for manufacturer in manufacturers:
        # Create or update an ManufacturerImport record based on the provided data
        manufacturer_record, _ = ManufacturerImport.objects.update_or_create(name=manufacturer)
        # Record the outcome in the JobResult record
        job_result.log(
            "Successfully created/updated manufacturer",
            obj=manufacturer_record,
            level_choice=LogLevelChoices.LOG_INFO,
            grouping="welcome_wizard",
        )
    for device_type, device_data in device_types.items():
        device_type_record, _ = DeviceTypeImport.objects.update_or_create(
            filename=device_type,
            name=device_data["model"],
            manufacturer=ManufacturerImport.objects.filter(name=device_data["manufacturer"])[0],
            defaults={"device_type_data": device_data},
        )
        job_result.log(
            "Successfully created/updated device_type",
            obj=device_type_record,
            level_choice=LogLevelChoices.LOG_INFO,
            grouping="welcome_wizard",
        )


# Register that records can be loaded from a Git repository,
# and register the callback function used to do so
datasource_contents = [
    (
        "extras.gitrepository",  # datasource class we are registering for
        DatasourceContent(
            name="Import Wizard",  # human-readable name to display in the UI
            content_identifier="welcome_wizard.import_wizard",  # internal slug to identify the data type
            icon="mdi-wizard-hat",  # Material Design Icons icon to use in UI
            callback=refresh_git_import_wizard,  # callback function on GitRepository refresh
        ),
    )
]
