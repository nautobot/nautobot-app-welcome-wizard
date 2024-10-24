"""API Serializers for Welcome Wizard."""

from rest_framework.serializers import ModelSerializer

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerImportSerializer(ModelSerializer):
    """API serializer for interacting with ManufacturerImport objects."""

    class Meta:
        """Meta for ManufacturerImport Serializer."""

        model = ManufacturerImport
        fields = ("id", "name")


class DeviceTypeImportSerializer(ModelSerializer):
    """API serializer for interacting with DeviceTypeImport Objects."""

    class Meta:
        """Meta for DeviceTypeImport Serializer."""

        model = DeviceTypeImport
        fields = ("id", "name", "filename", "manufacturer")
