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
    csv_data = (
        "name",
        "Test csv1",
        "Test csv2",
        "Test csv3",
    )

    @classmethod
    def setUpTestData(cls):
        fixtures.create_manufacturerimport()
