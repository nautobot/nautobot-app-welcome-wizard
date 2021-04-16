"""Merlin Tests."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models.merlin import Merlin
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


class MerlinModelTest(TestCase):
    """Model Test Case."""
    def test_base_setup_all_false(self):
        base = Merlin()
        self.assertFalse(base.manufacturers)
        self.assertFalse(base.platforms)
        self.assertFalse(base.all_completed)
        self.assertFalse(base.device_types)
        self.assertFalse(base.device_roles)
        self.assertFalse(base.rirs)
        self.assertFalse(base.cluster_types)
        self.assertFalse(base.circuit_types)
        self.assertFalse(base.providers)


class ManufacturerImportModelTest(TestCase):
    def test_manufacturer_setup(self):
        manufacturer = ManufacturerImport(name="Acme", slug="acme")
        self.assertEqual(manufacturer.name, "Acme")
        self.assertEqual(manufacturer.slug, "acme")
        self.assertEqual(str(manufacturer), "Acme")


class DeviceTypeImportModelTest(TestCase):
    def setUp(self):
        self.manufacturer = ManufacturerImport(name="Acme", slug="acme")

    def test_devicetype_setup(self):
        devicetype = DeviceTypeImport(
            name="FS12", filename="FS12.yaml", manufacturer=self.manufacturer, device_type_data={"test": "foo"}
        )
        self.assertEqual(devicetype.name, "FS12")
        self.assertEqual(devicetype.filename, "FS12.yaml")
        self.assertEqual(devicetype.manufacturer, self.manufacturer)
        self.assertEqual(devicetype.device_type_data, {"test": "foo"})
        self.assertEqual(str(devicetype), "FS12")

    def test_devicetype_invalid_data(self):
        devicetype = DeviceTypeImport(
            name="FS12", filename="FS12.yaml", manufacturer=self.manufacturer, device_type_data="bad_data"
        )
        with self.assertRaises(ValidationError):
            devicetype.clean()
