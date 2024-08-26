"""Test cases for Forms."""
from django.test import TestCase

from welcome_wizard.forms import DeviceTypeBulkImportForm, ManufacturerBulkImportForm
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerTestCase(TestCase):
    """Tests the ManufacturerImport Forms."""

    @classmethod
    def setUpTestData(cls):
        """Setup Testing data."""
        ManufacturerImport.objects.create(name="Acme", slug="acme")

    def test_manufacturer_bulk_import(self):
        """Ensure form with valid data is valid."""
        form = ManufacturerBulkImportForm(data={"pk": [ManufacturerImport.objects.first().pk]})

        self.assertTrue(form.is_valid())

    def test_manufacturer_bulk_import_invalid(self):
        """Ensure form with invalid data is invalid."""
        form = ManufacturerBulkImportForm(data={"pk": ""})

        self.assertFalse(form.is_valid())


class DeviceTypeTestCase(TestCase):
    """Tests the DeviceTypeImport Forms."""

    @classmethod
    def setUpTestData(cls):
        """Setup Testing data."""
        manufacturer = ManufacturerImport.objects.create(name="Acme", slug="acme")
        DeviceTypeImport.objects.create(
            filename="fs12.yml", name="FS12", manufacturer=manufacturer, device_type_data={"foo": "test"}
        )

    def test_devicetype_bulk_import(self):
        """Ensure form with valid data is valid."""
        form = DeviceTypeBulkImportForm(data={"pk": [DeviceTypeImport.objects.first().pk]})

        self.assertTrue(form.is_valid())

    def test_devicetype_bulk_import_invalid(self):
        """Ensure form with invalid data is invalid."""
        form = DeviceTypeBulkImportForm(data={"pk": ""})

        self.assertFalse(form.is_valid())
