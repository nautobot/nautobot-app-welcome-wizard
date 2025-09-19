"""Datasources for Welcome Wizard."""

import os
from pathlib import Path

import yaml
from django.conf import settings
from django.db.utils import IntegrityError
from nautobot.extras.choices import LogLevelChoices
from nautobot.extras.registry import DatasourceContent

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport, ModuleTypeImport


def get_manufacturer_name(name: str) -> str:
    """Get the manufacturer name to use based on settings.

    Args:
        name (str): Original manufacturer name from YAML configuration.

    Returns:
        str: Manufacturer name, possibly uppercased or transformed based on dictionary mapping.
    """
    manufacturer_name = name
    config = settings.PLUGINS_CONFIG.get("welcome_wizard", {})

    if config:
        manufacturer_map = config.get("manufacturer_map", {})
        if manufacturer_name in manufacturer_map:
            manufacturer_name = manufacturer_map[manufacturer_name]
        elif config.get("manufacturer_transform_func") and callable(config["manufacturer_transform_func"]):
            manufacturer_name = config["manufacturer_transform_func"](manufacturer_name)

    return manufacturer_name


def retrieve_device_types_from_filesystem(path):
    """Retrieve Manufacturers and Device Types from the file system.

    Args:
        path (str): Filesystem path to the repo holding the Device Types.

    Returns:
        tuple: a Set of Manufacturers and a dictionary of Device Types.
    """
    manufacturers = set()
    device_types = {}
    manufacturer_names = {}

    device_type_path = os.path.join(path, "device-types")
    files = (filename for filename in Path(device_type_path).rglob("*") if filename.suffix in [".yml", ".yaml"])

    for filename in files:
        with open(filename, encoding="utf8") as file:
            data = yaml.safe_load(file)

        # Transform manufacturer name based on settings if needed
        manufacturer_name = manufacturer_names.setdefault(
            data["manufacturer"], get_manufacturer_name(data["manufacturer"])
        )

        if data["manufacturer"] != manufacturer_name:
            # Update the manufacturer name in the data to the transformed name
            data["manufacturer"] = manufacturer_name

        manufacturers.add(manufacturer_name)
        device_types[filename.name] = data

    return (manufacturers, device_types)


def retrieve_module_types_from_filesystem(path):
    """Retrieve Manufacturers and Module Types from the file system.

    Args:
        path (str): Filesystem path to the repo holding the Module Types.

    Returns:
        tuple: a Set of Manufacturers and a dictionary of Module Types.
    """
    manufacturers = set()
    module_types = {}
    manufacturer_names = {}

    module_type_path = os.path.join(path, "module-types")
    files = (filename for filename in Path(module_type_path).rglob("*") if filename.suffix in [".yml", ".yaml"])

    for filename in files:
        with open(filename, encoding="utf8") as file:
            data = yaml.safe_load(file)

        # Transform manufacturer name based on settings if needed
        manufacturer_name = manufacturer_names.setdefault(
            data["manufacturer"], get_manufacturer_name(data["manufacturer"])
        )

        if data["manufacturer"] != manufacturer_name:
            # Update the manufacturer name in the data to the transformed name
            data["manufacturer"] = manufacturer_name

        manufacturers.add(manufacturer_name)
        module_types[filename.name] = data

    return (manufacturers, module_types)


def refresh_git_import_wizard(repository_record, job_result, delete=False):
    """Callback for GitRepository updates - refresh Device Types managed by it."""
    if "welcome_wizard.import_wizard" not in repository_record.provided_contents or delete:
        # TODO Handle delete.
        return

    manufacturers = {}

    # Refresh Device Types
    manufacturer_names, device_types = retrieve_device_types_from_filesystem(repository_record.filesystem_path)
    for manufacturer in manufacturer_names:
        # Create or update an ManufacturerImport record based on the provided data
        manufacturer_record = manufacturers.setdefault(
            manufacturer, ManufacturerImport.objects.update_or_create(name=manufacturer)[0]
        )
        # Record the outcome in the JobResult record
        job_result.log(
            "Successfully created/updated manufacturer",
            obj=manufacturer_record,
            level_choice=LogLevelChoices.LOG_INFO,
            grouping="welcome_wizard",
        )

    for device_type, device_data in device_types.items():
        try:
            device_type_record, _ = DeviceTypeImport.objects.update_or_create(
                filename=device_type,
                name=device_data["model"],
                manufacturer=manufacturers[device_data["manufacturer"]],
                defaults={"device_type_data": device_data},
            )
            job_result.log(
                "Successfully created/updated device_type",
                obj=device_type_record,
                level_choice=LogLevelChoices.LOG_INFO,
                grouping="welcome_wizard",
            )
        except IntegrityError as exc:
            job_result.log(
                f"Failed to create/update device_type {device_type} - {str(exc)}",
                level_choice=LogLevelChoices.LOG_WARNING,
                grouping="welcome_wizard",
            )

    # Refresh Module Types
    manufacturer_names, module_types = retrieve_module_types_from_filesystem(repository_record.filesystem_path)

    for manufacturer in manufacturer_names:
        # Create or update an ManufacturerImport record based on the provided data
        manufacturer_record = manufacturers.setdefault(
            manufacturer, ManufacturerImport.objects.update_or_create(name=manufacturer)[0]
        )
        # Record the outcome in the JobResult record
        job_result.log(
            "Successfully created/updated manufacturer",
            obj=manufacturer_record,
            level_choice=LogLevelChoices.LOG_INFO,
            grouping="welcome_wizard",
        )

    for module_type, module_data in module_types.items():
        try:
            module_type_record, _ = ModuleTypeImport.objects.update_or_create(
                filename=module_type,
                name=module_data["model"],
                manufacturer=manufacturers[module_data["manufacturer"]],
                defaults={"module_type_data": module_data},
            )
            job_result.log(
                "Successfully created/updated module_type",
                obj=module_type_record,
                level_choice=LogLevelChoices.LOG_INFO,
                grouping="welcome_wizard",
            )
        except IntegrityError as exc:
            job_result.log(
                f"Failed to create/update module_type {module_type} - {str(exc)}",
                level_choice=LogLevelChoices.LOG_WARNING,
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
