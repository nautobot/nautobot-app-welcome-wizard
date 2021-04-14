from nautobot.extras.jobs import Job, StringVar

from collections import OrderedDict
from django.utils.text import slugify
from merlin.models.importer import DeviceTypeImport

from nautobot.dcim.forms import DeviceTypeImportForm
from nautobot.dcim.models import (
    ConsolePortTemplate,
    ConsoleServerPortTemplate,
    DeviceBayTemplate,
    FrontPortTemplate,
    InterfaceTemplate,
    PowerOutletTemplate,
    PowerPortTemplate,
    RearPortTemplate,
    DeviceType,
    Manufacturer,
)


COMPONENTS = OrderedDict()
COMPONENTS['console-ports'] = ConsolePortTemplate
COMPONENTS['console-server-ports'] = ConsoleServerPortTemplate
COMPONENTS['power-ports'] = PowerPortTemplate
COMPONENTS['power-outlets'] = PowerOutletTemplate
COMPONENTS['interfaces'] = InterfaceTemplate
COMPONENTS['rear-ports'] = RearPortTemplate
COMPONENTS['front-ports'] = FrontPortTemplate
COMPONENTS['device-bays'] = DeviceBayTemplate


def import_device_type(data):
    """Import DeviceType."""
    slug = data.get("slug")

    try:
        devtype = DeviceType.objects.get(slug=data.get("slug"))
        raise ValueError(f"Unable to import this device_type, a DeviceType with this slug ({slug}) already exist.")
    except DeviceType.DoesNotExist:
        pass

    dtif = DeviceTypeImportForm(data)
    devtype = dtif.save()

    # Import All Components
    for key, component_class in COMPONENTS.items():
        if key in data:
            component_list = [
                component_class(device_type=devtype, **item)
                for item in data[key]
            ]
            component_class.objects.bulk_create(component_list)

    return devtype


class MerlinImportManufacturer(Job):

    class Meta:
        name = "Merlin - Import Manufacturer"
        description = "Imports a chosen Manufacturer"

    manufacturer = StringVar(
        description="Name of the new manufacturer"
    )

    def run(self, data, commit):
        # Create the new site
        manufacturer = Manufacturer.objects.update_or_create(
            name=data['manufacturer'],
            slug=slugify(data['manufacturer']),
        )
        self.log_success(obj=manufacturer, message="Created new manufacturer")

class MerlinImportDeviceType(Job):

    class Meta:
        name = "Merlin - Import Device Type"
        description = "Imports a chosen Device Type"

    device_type_filename = StringVar()

    def run(self, data=None, commit=None):
        """Main function for ImportDeviceType."""
        device_type = data.get("device_type", "none.yaml")

        data = DeviceTypeImport.objects.filter(filename=device_type)[0].device_type_data

        if "slug" not in data:
            self.log_error("The data returned is not valid, it should be a valid DeviceType in YAML format")
            return False

        slug = data.get("slug")
        try:
            devtype = import_device_type(data)
        except ValueError as exc:
            if 'already exist' not in str(exc):
                raise
            self.log_warning(
                message=f'Unable to import {device_type}, a DeviceType with this slug ({slug}) already exist.'
            )

            return False
        self.log_success(devtype, f"Imported DeviceType {slug} successfully")
