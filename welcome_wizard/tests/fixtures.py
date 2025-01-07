"""Create fixtures for tests."""

from welcome_wizard.models import ManufacturerImport


def create_manufacturerimport():
    """Fixture to create necessary number of ManufacturerImport for tests."""
    ManufacturerImport.objects.create(name="Test One")
    ManufacturerImport.objects.create(name="Test Two")
    ManufacturerImport.objects.create(name="Test Three")
