"""API Views for Welcome Wizard."""
from rest_framework.viewsets import ModelViewSet

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport
from .serializers import DeviceTypeImportSerializer, ManufacturerImportSerializer


class ManufacturerViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """API viewset for interacting with ManufacturerImport objects."""

    queryset = ManufacturerImport.objects.all()
    serializer_class = ManufacturerImportSerializer


class DeviceTypeViewSet(ModelViewSet):  # pylint: disable=too-many-ancestors
    """API viewset for interacting with DeviceTypeImport objects."""

    queryset = DeviceTypeImport.objects.all()
    serializer_class = DeviceTypeImportSerializer
