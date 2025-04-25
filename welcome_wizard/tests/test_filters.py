"""Test ManufacturerImport Filter."""

from nautobot.apps.testing import FilterTestCases

from welcome_wizard import filters, models
from welcome_wizard.tests import fixtures


class ManufacturerImportFilterTestCase(FilterTestCases.FilterTestCase):
    """ManufacturerImport Filter Test Case."""

    queryset = models.ManufacturerImport.objects.all()
    filterset = filters.ManufacturerImportFilterSet
    generic_filter_tests = (
        ("id",),
        ("created",),
        ("last_updated",),
        ("name",),
    )

    @classmethod
    def setUpTestData(cls):
        """Setup test data for ManufacturerImport Model."""
        fixtures.create_manufacturerimport()

    def test_q_search_name(self):
        """Test using Q search with name of ManufacturerImport."""
        params = {"q": "Test One"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_q_invalid(self):
        """Test using invalid Q search for ManufacturerImport."""
        params = {"q": "test-five"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 0)
