"""Unit tests for welcome_wizard."""

from nautobot.apps.testing import APIViewTestCases

from welcome_wizard import models
from welcome_wizard.tests import fixtures


class ManufacturerImportAPIViewTest(APIViewTestCases.APIViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the API viewsets for ManufacturerImport."""

    model = models.ManufacturerImport
    create_data = [
        {
            "name": "Test Model 1",
            "description": "test description",
        },
        {
            "name": "Test Model 2",
        },
    ]
    bulk_update_data = {"description": "Test Bulk Update"}

    @classmethod
    def setUpTestData(cls):
        fixtures.create_manufacturerimport()
