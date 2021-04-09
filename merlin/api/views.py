from rest_framework.viewsets import ModelViewSet

from merlin.models.importer import DeviceTypeImport, ManufacturerImport
from .serializers import DeviceTypeImportSerializer, ManufacturerImportSerializer


class ManufacturerViewSet(ModelViewSet):
    """API viewset for interacting with Animal objects."""

    queryset = ManufacturerImport.objects.all()
    serializer_class = ManufacturerImportSerializer

class DeviceTypeViewSet(ModelViewSet):
    """API viewset for interacting with Animal objects."""

    queryset = DeviceTypeImport.objects.all()
    serializer_class = DeviceTypeImportSerializer