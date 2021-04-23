"""Merlin Tests."""
from django.test import TestCase
from django.core.exceptions import ValidationError

from merlin.models.merlin import Merlin
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


class MerlinModelTest(TestCase):
    """Model Test Case."""

    def test_base_setup_only_name_supplied(self):
        """Validate empty Merlin model."""
        merlin = Merlin.objects.create(name="Sites")
        self.assertEqual(merlin.name, "Sites")
        self.assertFalse(merlin.completed)
        self.assertFalse(merlin.ignored)
        self.assertEqual(merlin.nautobot_model, "")
        self.assertEqual(merlin.nautobot_add_link, "")
        self.assertEqual(merlin.merlin_link, "")

    def test_base_setup_complete(self):
        """Validate empty Merlin model."""
        merlin = Merlin.objects.create(
            name="Sites",
            completed=True,
            ignored=False,
            nautobot_model="dcim:sites_list",
            nautobot_add_link="dcim:sites_add",
            merlin_link="plugins:merlin:devicetype_import",
        )
        self.assertEqual(merlin.name, "Sites")
        self.assertTrue(merlin.completed)
        self.assertFalse(merlin.ignored)
        self.assertEqual(merlin.nautobot_model, "dcim:sites_list")
        self.assertEqual(merlin.nautobot_add_link, "dcim:sites_add")
        self.assertEqual(merlin.merlin_link, "plugins:merlin:devicetype_import")


class ManufacturerImportModelTest(TestCase):
    """ManufacturerImport Model Tests."""

    def test_manufacturer_setup(self):
        """Run Tests."""
        manufacturer = ManufacturerImport(name="Acme", slug="acme")
        self.assertEqual(manufacturer.name, "Acme")
        self.assertEqual(manufacturer.slug, "acme")
        self.assertEqual(str(manufacturer), "Acme")


class DeviceTypeImportModelTest(TestCase):
    """DeviceTypeImport Model Tests."""

    def setUp(self):
        """Setup ManufacturerImport for tests."""
        self.manufacturer = ManufacturerImport(name="Acme", slug="acme")

    def test_devicetype_setup(self):
        """Run Tests with valid data."""
        devicetype = DeviceTypeImport(
            name="FS12", filename="FS12.yaml", manufacturer=self.manufacturer, device_type_data={"test": "foo"}
        )
        self.assertEqual(devicetype.name, "FS12")
        self.assertEqual(devicetype.filename, "FS12.yaml")
        self.assertEqual(devicetype.manufacturer, self.manufacturer)
        self.assertEqual(devicetype.device_type_data, {"test": "foo"})
        self.assertEqual(str(devicetype), "FS12")

    def test_devicetype_invalid_data(self):
        """Run Tests with invalid data."""
        devicetype = DeviceTypeImport(
            name="FS12", filename="FS12.yaml", manufacturer=self.manufacturer, device_type_data="bad_data"
        )
        with self.assertRaises(ValidationError):
            devicetype.clean()
