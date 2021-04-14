import django_filters

from django.db.models import Q
from nautobot.utilities.filters import BaseFilterSet, NameSlugSearchFilterSet
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerImportFilterSet(BaseFilterSet,
    NameSlugSearchFilterSet,
):
    class Meta:
        model = ManufacturerImport
        fields = ["id", "name", "slug"]

class DeviceTypeImportFilterSet(BaseFilterSet):
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
        model = DeviceTypeImport
        fields = [
            "id",
            "name",
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(manufacturer__name__icontains=value)
        )