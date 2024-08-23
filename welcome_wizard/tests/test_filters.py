"""Test Welcome Wizard Filters."""
from django.test import TestCase

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport
from welcome_wizard.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet


class ManufacturerTestCase(TestCase):
    """ManufacturerImport Filters."""

    queryset = ManufacturerImport.objects.all()
    filterset = ManufacturerImportFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup Data."""
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        ManufacturerImport.objects.create(name="Acme1", slug="acme1")
        ManufacturerImport.objects.create(name="Test", slug="test")

    def test_id(self):
        """Test filtering by ID."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_name(self):
        """Test filtering by Name."""
        params = {"name": ["Acme", "Test", "Acme1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_slug(self):
        """Test filtering by Slug."""
        params = {"slug": ["acme1", "test"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)


class DeviceTypeTestCase(TestCase):
    """DeviceTypeImport Filters."""

    queryset = DeviceTypeImport.objects.all()
    filterset = DeviceTypeImportFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup Data."""
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
        """Test filtering by ID."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_name(self):
        """Test filtering by Name."""
        params = {"name": ["testing", "fake", "FS12"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_manufacturer(self):
        """Test filtering by Manufacturer."""
        manufacturers = ManufacturerImport.objects.all()[:2]
        params = {"manufacturer_id": [manufacturers[0].pk, manufacturers[1].pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)
        params = {"manufacturers": [manufacturers[0].slug, manufacturers[1].slug]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_search(self):
        """Test the search ability."""
        params = {"q": "test"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
