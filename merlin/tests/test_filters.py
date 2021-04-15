from django.test import TestCase

from merlin.models.importer import DeviceTypeImport, ManufacturerImport
from merlin.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet


class ManufacturerTestCase(TestCase):
    queryset = ManufacturerImport.objects.all()
    filterset = ManufacturerImportFilterSet

    @classmethod
    def setUpTestData(cls):
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        ManufacturerImport.objects.create(name="Acme1", slug="acme1")
        ManufacturerImport.objects.create(name="Test", slug="test")

    def test_id(self):
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_name(self):
        params = {"name": ["Acme", "Test", "Acme1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_slug(self):
        params = {"slug": ["acme1", "test"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class DeviceTypeTestCase(TestCase):
    queryset = DeviceTypeImport.objects.all()
    filterset = DeviceTypeImportFilterSet

    @classmethod
    def setUpTestData(cls):
        manufacturers = (
            ManufacturerImport.objects.create(name="Acme", slug="acme"),
            ManufacturerImport.objects.create(name="Test", slug="test"),
        )

        DeviceTypeImport.objects.create(
            filename="testing.yml", name="testing", manufacturer=manufacturers[1], device_type_data={"foo": "test"}
        )

        DeviceTypeImport.objects.create(
            filename="fake.yml", name="fake", manufacturer=manufacturers[1], device_type_data={"foo": "test"}
        )

        DeviceTypeImport.objects.create(
            filename="fs12.yml", name="FS12", manufacturer=manufacturers[0], device_type_data={"foo": "test"}
        )

    def test_id(self):
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_name(self):
        params = {"name": ["testing", "fake", "FS12"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_manufacturer(self):
        manufacturers = ManufacturerImport.objects.all()[:2]
        params = {"manufacturer_id": [manufacturers[0].pk, manufacturers[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"manufacturers": [manufacturers[0].slug, manufacturers[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_search(self):
        params = {"q": "test"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
