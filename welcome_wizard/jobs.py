"""Background Jobs for Welcome Wizard."""

import contextlib
from collections import OrderedDict

from django.db import IntegrityError
from nautobot.apps.jobs import Job, StringVar
from nautobot.core.celery import register_jobs
from nautobot.dcim.forms import DeviceTypeImportForm
from nautobot.dcim.models import (
    ConsolePortTemplate,
    ConsoleServerPortTemplate,
    DeviceBayTemplate,
    DeviceType,
    FrontPortTemplate,
    InterfaceTemplate,
    Manufacturer,
    ModuleBayTemplate,
    PowerOutletTemplate,
    PowerPortTemplate,
    RearPortTemplate,
)

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
COMPONENTS["module-bays"] = ModuleBayTemplate


def import_components(device_type: DeviceType, data: dict):
    """Import components for a given device type."""
    for key, component_class in COMPONENTS.items():
        if key in data:
            component_list = []

            for item in data[key]:
                item_data = {k: v for k, v in item.items() if hasattr(component_class, k)}

                if key == "power-outlets" and "power_port" in item:
                    # Special case for PowerOutletTemplate to handle the FK to PowerPortTemplate
                    try:
                        item_data["power_port_template"] = PowerPortTemplate.objects.get(
                            device_type=device_type, name=item["power_port"]
                        )
                    except PowerPortTemplate.DoesNotExist as exc:
                        raise ValueError(
                            f"PowerPortTemplate with name '{item['power_port']}' does not exist for DeviceType '{device_type}'."
                        ) from exc

                elif key == "front-ports" and "rear_port" in item:
                    # Special case for FrontPortTemplate to handle the FK to RearPortTemplate
                    try:
                        item_data["rear_port_template"] = RearPortTemplate.objects.get(
                            device_type=device_type, name=item["rear_port"]
                        )
                    except RearPortTemplate.DoesNotExist as exc:
                        raise ValueError(
                            f"RearPortTemplate with name '{item['rear_port']}' does not exist for DeviceType '{device_type}'."
                        ) from exc

                component_list.append(component_class(device_type=device_type, **item_data))

            try:
                component_class.objects.bulk_create(component_list)
            except IntegrityError as exc:
                raise ValueError(f"Failed to create {component_class.__name__} component(s): {str(exc)}") from exc


def import_device_type(data: dict) -> None:
    """Import DeviceType."""
    manufacturer = Manufacturer.objects.get(name=data.get("manufacturer"))
    model = data.get("model")
    with contextlib.suppress(DeviceType.DoesNotExist):
        devtype = DeviceType.objects.get(model=model, manufacturer=manufacturer)
        raise ValueError(
            f"Unable to import this device_type, a DeviceType with this model ({model}) and manufacturer ({manufacturer}) already exist."
        )
    dtif = DeviceTypeImportForm(data)
    devtype = dtif.save()

    # Import All Components
    import_components(devtype, data)


name = "Welcome Wizard"  # pylint: disable=invalid-name


class WelcomeWizardImportManufacturer(Job):
    """Manufacturer Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Manufacturer Import."""

        name = "Welcome Wizard - Import Manufacturer"
        description = "Imports a chosen Manufacturer (Run from the Welcome Wizard Dashboard)"

    manufacturer_name = StringVar(description="Name of the new manufacturer")

    def run(self, manufacturer_name):  # pylint: disable=arguments-differ
        """Tries to import the selected Manufacturer into Nautobot."""
        # Create the new manufacturer
        manufacturer, _ = Manufacturer.objects.update_or_create(
            name=manufacturer_name,
        )
        self.logger.info("Created new manufacturer", extra={"object": manufacturer})


class WelcomeWizardImportDeviceType(Job):
    """Device Type Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Device Type Import."""

        name = "Welcome Wizard - Import Device Type"
        description = "Imports a chosen Device Type (Run from the Welcome Wizard Dashboard)"

    filename = StringVar()

    def run(self, filename):  # pylint: disable=arguments-differ
        """Tries to import the selected Device Type into Nautobot."""
        device_type = filename if filename else "none.yaml"
        device_type_data = DeviceTypeImport.objects.filter(filename=device_type)[0].device_type_data
        manufacturer = device_type_data.get("manufacturer")
        model = device_type_data.get("model")

        Manufacturer.objects.update_or_create(name=manufacturer)

        self.logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Importing {manufacturer} DeviceType {model}", extra={"object": device_type_data}
        )
        try:
            import_device_type(device_type_data)
        except (ValueError, IntegrityError) as exc:
            self.logger.error(str(exc))
            raise exc

        self.logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Imported {manufacturer} DeviceType {model} successfully"
        )


register_jobs(WelcomeWizardImportManufacturer, WelcomeWizardImportDeviceType)
