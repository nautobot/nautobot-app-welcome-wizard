"""API Serializers for Merlin."""
from rest_framework.serializers import ModelSerializer

from merlin.models.importer import ManufacturerImport, DeviceTypeImport


class ManufacturerImportSerializer(ModelSerializer):
    """API serializer for interacting with ManufacturerImport objects."""

    class Meta:
        """Meta for ManufacturerImport Serializer."""

        model = ManufacturerImport
        fields = ("id", "name", "slug")


class DeviceTypeImportSerializer(ModelSerializer):
    """API serializer for interacting with DeviceTypeImport Objects."""

    class Meta:
        """Meta for DeviceTypeImport Serializer."""

        model = DeviceTypeImport
        fields = ("id", "name", "filename", "manufacturer")
