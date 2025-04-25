"""Unit tests for views."""

from nautobot.apps.testing import ViewTestCases

from welcome_wizard import models
from welcome_wizard.tests import fixtures


class ManufacturerImportViewTest(ViewTestCases.PrimaryObjectViewTestCase):
    # pylint: disable=too-many-ancestors
    """Test the ManufacturerImport views."""

    model = models.ManufacturerImport
    bulk_edit_data = {"description": "Bulk edit views"}
    form_data = {
        "name": "Test 1",
        "description": "Initial model",
    }

    update_data = {
        "name": "Test 2",
        "description": "Updated model",
    }

    @classmethod
    def setUpTestData(cls):
        fixtures.create_manufacturerimport()
