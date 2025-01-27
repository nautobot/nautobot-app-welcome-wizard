"""API views for welcome_wizard."""

from nautobot.apps.api import NautobotModelViewSet

from welcome_wizard import filters, models
from welcome_wizard.api import serializers


class ManufacturerImportViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ManufacturerImport viewset."""

    queryset = models.ManufacturerImport.objects.all()
    serializer_class = serializers.ManufacturerImportSerializer
    filterset_class = filters.ManufacturerImportFilterSet


class DeviceTypeImportViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """DeviceTypeImport viewset."""

    queryset = models.DeviceTypeImport.objects.all()
    serializer_class = serializers.DeviceTypeImportSerializer
    filterset_class = filters.DeviceTypeImportFilterSet
