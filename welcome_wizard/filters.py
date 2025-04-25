"""Filtering for welcome_wizard."""

from nautobot.apps.filters import (
    NameSearchFilterSet,
    NaturalKeyOrPKMultipleChoiceFilter,
    NautobotFilterSet,
    SearchFilter,
)

from welcome_wizard import models


class ManufacturerImportFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for ManufacturerImport."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ManufacturerImport

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
