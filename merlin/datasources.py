import yaml
import os

from django.utils.text import slugify
from nautobot.extras.choices import LogLevelChoices
from nautobot.extras.registry import DatasourceContent
from pathlib import Path

from merlin.models.importer import ManufacturerImport, DeviceTypeImport


def refresh_git_device_type_importer(repository_record, job_result, delete=False):
    """Callback for GitRepository updates - refresh Device Types managed by it."""
    if 'merlin.device_type_importer' not in repository_record.provided_contents:
        # This repository is defined not to provide Animal records.
        # In a more complete worked example, we might want to iterate over any
        # Animals that might have been previously created by this GitRepository
        # and ensure their deletion, but for now this is a no-op.
        return

    manufacturers = set()
    device_types = {}

    # We have decided that a Git repository can provide YAML files in a
    # /animals/ directory at the repository root.
    device_type_path = os.path.join(repository_record.filesystem_path, 'device-types')
    for filename in Path(device_type_path).rglob('*.yaml'):
        with open(filename) as fd:
            data = yaml.safe_load(fd)

        manufacturers.add(data['manufacturer'])
        device_types[filename.name] = data

    for manufacturer in manufacturers:
        # Create or update an ManufacturerImport record based on the provided data
        manufacturer_record, created = ManufacturerImport.objects.update_or_create(
            name=manufacturer,
            slug=slugify(manufacturer)
        )

        # Record the outcome in the JobResult record
        job_result.log(
            "Successfully created/updated manufacturer",
            obj=manufacturer_record,
            level_choice=LogLevelChoices.LOG_SUCCESS,
            grouping="merlin",
        )
    
    for device_type, device_data in device_types.items():
        device_type_record, created = DeviceTypeImport.objects.update_or_create(
            filename=device_type,
            name=device_data['model'],
            manufacturer=ManufacturerImport.objects.filter(name=device_data['manufacturer'])[0],
            device_type_data=device_data
        )
        job_result.log(
            "Successfully created/updated device_type",
            obj=device_type_record,
            level_choice=LogLevelChoices.LOG_SUCCESS,
            grouping="merlin",
        )

# Register that Animal records can be loaded from a Git repository,
# and register the callback function used to do so
datasource_contents = [
    (
        'extras.gitrepository',                                # datasource class we are registering for
        DatasourceContent(
            name='device type importer',                                    # human-readable name to display in the UI
            content_identifier='merlin.device_type_importer',  # internal slug to identify the data type
            icon='mdi-paw',                                    # Material Design Icons icon to use in UI
            callback=refresh_git_device_type_importer,                      # callback function on GitRepository refresh
        )
    )
]
