"""Test Welcome Wizard Filters."""

from django.test import TestCase

from welcome_wizard.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerTestCase(TestCase):
    """ManufacturerImport Filters."""

    queryset = ManufacturerImport.objects.all()
    filterset = ManufacturerImportFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup Data."""
        ManufacturerImport.objects.create(name="Acme")
        ManufacturerImport.objects.create(name="Acme1")
        ManufacturerImport.objects.create(name="Test")

    def test_id(self):
        """Test filtering by ID."""
        params = {"id": self.queryset.values_list("pk", flat=True)[:2]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_name(self):
        """Test filtering by Name."""
        params = {"name": ["Acme", "Test", "Acme1"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)


class DeviceTypeTestCase(TestCase):
    """DeviceTypeImport Filters."""

    queryset = DeviceTypeImport.objects.all()
    filterset = DeviceTypeImportFilterSet

    @classmethod
    def setUpTestData(cls):
        """Setup Data."""
        manufacturers = (
            ManufacturerImport.objects.create(name="Acme"),
            ManufacturerImport.objects.create(name="Test"),
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
        """Test filtering by Manufacturer name.

        Regression test: filtering by manufacturer name returned an empty list because the
        filter's `field_name` was `manufacturer__name` instead of the FK field `manufacturer`.
        """
        params = {"manufacturer": ["Test"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
        params = {"manufacturer": ["Acme"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        # NaturalKeyOrPKMultipleChoiceFilter also supports filtering by primary key.
        test = ManufacturerImport.objects.get(name="Test")
        params = {"manufacturer": [test.pk]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)

    def test_search(self):
        """Test the search ability."""
        params = {"q": "test"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 2)
