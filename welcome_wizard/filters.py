"""Filters for Welcome Wizard."""

import django_filters

from django.db.models import Q
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerImportFilterSet(
    BaseFilterSet,
    NameSlugSearchFilterSet,
):
    """Manufacturer Import Filter Set."""

    class Meta:
        """Meta for Manufacturer Import Filter Set."""

        model = ManufacturerImport
        fields = ["id", "name", "slug"]


class DeviceTypeImportFilterSet(BaseFilterSet):
    """Device Type Import Filter Set."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ManufacturerImport.objects.all(),
        label="Manufacturer (ID)",
    )
    manufacturer = django_filters.ModelMultipleChoiceFilter(
        field_name="manufacturer__slug",
        queryset=ManufacturerImport.objects.all(),
        to_field_name="slug",
        label="Manufacturer (slug)",
    )

    class Meta:
        """Meta for Device Type Import Filter Set."""

        model = DeviceTypeImport
        fields = [
            "id",
            "name",
        ]

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Search for Device Type where name or manufacturer contain value."""
        # Nautobot search function, not sure where name and self should be used.
        return queryset.filter(Q(name__icontains=value) | Q(manufacturer__name__icontains=value))
