"""Background Jobs for Welcome Wizard."""

import contextlib
from collections import OrderedDict

from nautobot.apps.jobs import Job, StringVar
from nautobot.core.celery import register_jobs
from nautobot.dcim.forms import DeviceTypeImportForm, ModuleTypeImportForm
from nautobot.dcim.models import (
    ConsolePortTemplate,
    ConsoleServerPortTemplate,
    DeviceBayTemplate,
    DeviceType,
    FrontPortTemplate,
    InterfaceTemplate,
    Manufacturer,
    ModuleBayTemplate,
    ModuleType,
    PowerOutletTemplate,
    PowerPortTemplate,
    RearPortTemplate,
)

from welcome_wizard.models.importer import DeviceTypeImport, ModuleTypeImport

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

STRIP_KEYWORDS = {
    "interfaces": ["poe_mode", "poe_type"],
}


def import_device_type(data):
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


def import_module_type(data):
    """Import ModuleType."""
    manufacturer = Manufacturer.objects.get(name=data.get("manufacturer"))
    model = data.get("model")
    with contextlib.suppress(ModuleType.DoesNotExist):
        modtype = ModuleType.objects.get(model=model, manufacturer=manufacturer)
        raise ValueError(
            f"Unable to import this module_type, a ModuleType with this model ({model}) and manufacturer ({manufacturer}) already exist."
        )
    mtif = ModuleTypeImportForm(data)
    modtype = mtif.save()

    # Import All Components
    for key, component_class in COMPONENTS.items():
        if key in data:
            component_list = [
                component_class(
                    module_type=modtype,
                    **{k: v for k, v in item.items() if k not in STRIP_KEYWORDS.get(key, [])},
                )
                for item in data[key]
            ]
            component_class.objects.bulk_create(component_list)
    return modtype


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
        # device_type = data.get("device_type_filename", "none.yaml")
        device_type = filename if filename else "none.yaml"

        device_type_data = DeviceTypeImport.objects.filter(filename=device_type)[0].device_type_data

        manufacturer = device_type_data.get("manufacturer")
        Manufacturer.objects.update_or_create(
            name=manufacturer,
        )

        try:
            devtype = import_device_type(device_type_data)
        except ValueError as exc:
            self.logger.error(str(exc))
            raise exc

        self.logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Imported DeviceType {device_type_data.get('model')} successfully", extra={"object": devtype}
        )


class WelcomeWizardImportModuleType(Job):
    """Module Type Import."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta for Module Type Import."""

        name = "Welcome Wizard - Import Module Type"
        description = "Imports a chosen Module Type (Run from the Welcome Wizard Dashboard)"

    filename = StringVar()

    def run(self, filename):  # pylint: disable=arguments-differ
        """Tries to import the selected Module Type into Nautobot."""
        module_type = filename if filename else "none.yaml"

        module_type_data = ModuleTypeImport.objects.filter(filename=module_type)[0].module_type_data

        manufacturer = module_type_data.get("manufacturer")
        Manufacturer.objects.update_or_create(
            name=manufacturer,
        )

        try:
            modtype = import_module_type(module_type_data)
        except ValueError as exc:
            self.logger.error(str(exc))
            raise exc

        self.logger.info(  # pylint: disable=logging-fstring-interpolation
            f"Imported ModuleType {module_type_data.get('model')} successfully", extra={"object": modtype}
        )


register_jobs(WelcomeWizardImportManufacturer, WelcomeWizardImportDeviceType, WelcomeWizardImportModuleType)
