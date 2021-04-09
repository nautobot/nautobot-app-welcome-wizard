from rest_framework.serializers import ModelSerializer

from merlin.models.importer import ManufacturerImport, DeviceTypeImport


class ManufacturerImportSerializer(ModelSerializer):
    """API serializer for interacting with ManufacturerImport objects."""

    class Meta:
        model = ManufacturerImport
        fields = ('id', 'name', 'slug')

class DeviceTypeImportSerializer(ModelSerializer):
    """API serializer for interacting with DeviceTypeImport Objects"""

    class Meta:
        model = DeviceTypeImport
        fields = ('id', 'name', 'filename', 'manufacturer')
