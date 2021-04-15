from django.test import TestCase

from merlin.forms import DeviceTypeBulkImportForm, ManufacturerBulkImportForm
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        ManufacturerImport.objects.create(name="Acme", slug="acme")

    def test_manufacturer_bulk_import(self):
        form = ManufacturerBulkImportForm(data={"pk": [ManufacturerImport.objects.first().pk]})

        self.assertTrue(form.is_valid())

    def test_manufacturer_bulk_import_invalid(self):
        form = ManufacturerBulkImportForm(data={"pk": ""})

        self.assertFalse(form.is_valid())


class DeviceTypeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = ManufacturerImport.objects.create(name="Acme", slug="acme")
        DeviceTypeImport.objects.create(
            filename="fs12.yml", name="FS12", manufacturer=manufacturer, device_type_data={"foo": "test"}
        )

    def test_devicetype_bulk_import(self):
        form = DeviceTypeBulkImportForm(data={"pk": [DeviceTypeImport.objects.first().pk]})

        self.assertTrue(form.is_valid())

    def test_devicetype_bulk_import_invalid(self):
        form = DeviceTypeBulkImportForm(data={"pk": ""})

        self.assertFalse(form.is_valid())
