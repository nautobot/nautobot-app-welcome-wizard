"""Test ManufacturerImport."""

from django.test import TestCase

from welcome_wizard import models


class TestManufacturerImport(TestCase):
    """Test ManufacturerImport."""

    def test_create_manufacturerimport_only_required(self):
        """Create with only required fields, and validate null description and __str__."""
        manufacturerimport = models.ManufacturerImport.objects.create(name="Development")
        self.assertEqual(manufacturerimport.name, "Development")
        self.assertEqual(manufacturerimport.description, "")
        self.assertEqual(str(manufacturerimport), "Development")

    def test_create_manufacturerimport_all_fields_success(self):
        """Create ManufacturerImport with all fields."""
        manufacturerimport = models.ManufacturerImport.objects.create(name="Development", description="Development Test")
        self.assertEqual(manufacturerimport.name, "Development")
        self.assertEqual(manufacturerimport.description, "Development Test")
