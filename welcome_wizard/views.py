"""Views for welcome_wizard."""

from nautobot.apps.views import NautobotUIViewSet

from welcome_wizard import filters, forms, models, tables
from welcome_wizard.api import serializers


class ManufacturerImportUIViewSet(NautobotUIViewSet):
    """ViewSet for ManufacturerImport views."""

    bulk_update_form_class = forms.ManufacturerImportBulkEditForm
    filterset_class = filters.ManufacturerImportFilterSet
    filterset_form_class = forms.ManufacturerImportFilterForm
    form_class = forms.ManufacturerImportForm
    lookup_field = "pk"
    queryset = models.ManufacturerImport.objects.all()
    serializer_class = serializers.ManufacturerImportSerializer
    table_class = tables.ManufacturerImportTable
