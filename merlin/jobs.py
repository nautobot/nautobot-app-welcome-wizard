"""Background Jobs for Merlin."""

from collections import OrderedDict
from django.utils.text import slugify
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
from nautobot.extras.jobs import Job, StringVar
from merlin.models.importer import DeviceTypeImport


COMPONENTS = OrderedDict()
COMPONENTS["console-ports"] = ConsolePortTemplate
COMPONENTS["console-server-ports"] = ConsoleServerPortTemplate
COMPONENTS["power-ports"] = PowerPortTemplate
COMPONENTS["power-outlets"] = PowerOutletTemplate
COMPONENTS["interfaces"] = InterfaceTemplate
COMPONENTS["rear-ports"] = RearPortTemplate
COMPONENTS["front-ports"] = FrontPortTemplate
COMPONENTS["device-bays"] = DeviceBayTemplate


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
            component_list = [component_class(device_type=devtype, **item) for item in data[key]]
            component_class.objects.bulk_create(component_list)

    return devtype


class MerlinImportManufacturer(Job):
    """Manufacturer Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Manufacturer Import."""

        name = "Merlin - Import Manufacturer"
        description = "Imports a chosen Manufacturer"

    manufacturer = StringVar(description="Name of the new manufacturer")

    def run(self, data, commit):
        """Tries to import the selected Manufacturer into Nautobot."""
        # Create the new site
        manufacturer = Manufacturer.objects.update_or_create(
            name=data["manufacturer"],
            slug=slugify(data["manufacturer"]),
        )
        self.log_success(obj=manufacturer, message="Created new manufacturer")


class MerlinImportDeviceType(Job):
    """Device Type Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Device Type Import."""

        name = "Merlin - Import Device Type"
        description = "Imports a chosen Device Type"

    device_type_filename = StringVar()

    def run(self, data, commit=None):  # pylint: disable=inconsistent-return-statements
        """Tries to import the selected Device Type into Nautobot."""
        device_type = data.get("device_type", "none.yaml")

        data = DeviceTypeImport.objects.filter(filename=device_type)[0].device_type_data

        slug = data.get("slug")
        try:
            devtype = import_device_type(data)
        except ValueError as exc:
            if "already exist" not in str(exc):
                raise
            self.log_warning(
                message=f"Unable to import {device_type}, a DeviceType with this slug ({slug}) already exist."
            )

            return False
        self.log_success(devtype, f"Imported DeviceType {slug} successfully")
