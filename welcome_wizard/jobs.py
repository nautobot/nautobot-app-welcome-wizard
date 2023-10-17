"""Background Jobs for Welcome Wizard."""


import contextlib
from collections import OrderedDict
from nautobot.core.celery import register_jobs
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
from welcome_wizard.models.importer import DeviceTypeImport


COMPONENTS = OrderedDict()
COMPONENTS["console-ports"] = ConsolePortTemplate
COMPONENTS["console-server-ports"] = ConsoleServerPortTemplate
COMPONENTS["power-ports"] = PowerPortTemplate
COMPONENTS["power-outlets"] = PowerOutletTemplate
COMPONENTS["interfaces"] = InterfaceTemplate
COMPONENTS["rear-ports"] = RearPortTemplate
COMPONENTS["front-ports"] = FrontPortTemplate
COMPONENTS["device-bays"] = DeviceBayTemplate

STRIP_KEYWORDS = {
    "interfaces": ["poe_mode", "poe_type"],
}


def import_device_type(data):
    """Import DeviceType."""
    manufacturer = Manufacturer.objects.get(data.get("manufacturer"))
    model = data.get("model")
    with contextlib.suppress(DeviceType.DoesNotExist):
        devtype = DeviceType.objects.get(model=model, manufacturer=manufacturer)
        raise ValueError(f"Unable to import this device_type, a DeviceType with this model ({model}) and manufacturer ({manufacturer}) already exist.")
    dtif = DeviceTypeImportForm(data)
    devtype = dtif.save()

    # Import All Components
    for key, component_class in COMPONENTS.items():
        if key in data:
            component_list = [
                component_class(
                    device_type=devtype,
                    **{k: v for k, v in item.items() if k not in STRIP_KEYWORDS.get(key, [])},
                )
                for item in data[key]
            ]
            component_class.objects.bulk_create(component_list)

    return devtype


class WelcomeWizardImportManufacturer(Job):
    """Manufacturer Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Manufacturer Import."""

        name = "Welcome Wizard - Import Manufacturer"
        description = "Imports a chosen Manufacturer"

    manufacturer = StringVar(description="Name of the new manufacturer")

    def run(self, **data):
        """Tries to import the selected Manufacturer into Nautobot."""
        # Create the new site
        manufacturer = Manufacturer.objects.update_or_create(
            name=data["manufacturer"],
        )
        self.logger.info("Created new manufacturer", extra={"object": manufacturer})


class WelcomeWizardImportDeviceType(Job):
    """Device Type Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Device Type Import."""

        name = "Welcome Wizard - Import Device Type"
        description = "Imports a chosen Device Type"

    device_type_filename = StringVar()

    def run(self, **data):  # pylint: disable=inconsistent-return-statements
        """Tries to import the selected Device Type into Nautobot."""
        device_type = data.get("device_type_filename", "none.yaml")

        device_type_data = DeviceTypeImport.objects.filter(filename=device_type)[0].device_type_data

        manufacturer = device_type_data.get("manufacturer")
        Manufacturer.objects.update_or_create(
            name=manufacturer,
        )

        try:
            devtype = import_device_type(device_type_data)
        except ValueError as exc:
            self.logger.error(
                f"Unable to import {device_type}, a DeviceType with this model and manufacturer ({manufacturer}) already exist. {exc}"
            )
            raise exc

        self.logger.info(f"Imported DeviceType {device_type_data.get('model')} successfully", extra={"object": devtype})

register_jobs(WelcomeWizardImportManufacturer, WelcomeWizardImportDeviceType)
