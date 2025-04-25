"""Test ManufacturerImport."""

from nautobot.apps.testing import ModelTestCases

from welcome_wizard import models
from welcome_wizard.tests import fixtures


class TestManufacturerImport(ModelTestCases.BaseModelTestCase):
    """Test ManufacturerImport."""

    model = models.ManufacturerImport

    @classmethod
    def setUpTestData(cls):
        """Create test data for ManufacturerImport Model."""
        super().setUpTestData()
        # Create 3 objects for the model test cases.
        fixtures.create_manufacturerimport()

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
