"""Test manufacturerimport forms."""

from django.test import TestCase

from welcome_wizard import forms


class ManufacturerImportTest(TestCase):
    """Test ManufacturerImport forms."""

    def test_specifying_all_fields_success(self):
        form = forms.ManufacturerImportForm(
            data={
                "name": "Development",
                "description": "Development Testing",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_specifying_only_required_success(self):
        form = forms.ManufacturerImportForm(
            data={
                "name": "Development",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_validate_name_manufacturerimport_is_required(self):
        form = forms.ManufacturerImportForm(data={"description": "Development Testing"})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["name"])
