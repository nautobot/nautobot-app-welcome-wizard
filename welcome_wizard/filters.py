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


class DeviceTypeImportFilterSet(NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for DeviceTypeImport."""

    q = SearchFilter(
        filter_predicates={
            "manufacturer__name": "icontains",
            "name": "icontains",
        }
    )
    manufacturer = NaturalKeyOrPKMultipleChoiceFilter(
        to_field_name="name",
        queryset=models.ManufacturerImport.objects.all(),
        field_name="manufacturer__name",
        label="Manufacturer",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.DeviceTypeImport

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"


class MerlinFilterSet(NautobotFilterSet):
    """Filter for Merlin."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Merlin

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
