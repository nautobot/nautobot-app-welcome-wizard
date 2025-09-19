"""API serializers for welcome_wizard."""

from nautobot.apps.api import NautobotModelSerializer

from welcome_wizard import models


class ManufacturerImportSerializer(NautobotModelSerializer):  # pylint: disable=too-many-ancestors
    """ManufacturerImport Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ManufacturerImport
        fields = "__all__"


class DeviceTypeImportSerializer(NautobotModelSerializer):  # pylint: disable=too-many-ancestors
    """DeviceTypeImport Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.DeviceTypeImport
        fields = "__all__"


class ModuleTypeImportSerializer(NautobotModelSerializer):  # pylint: disable=too-many-ancestors
    """ModuleTypeImport Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ModuleTypeImport
        fields = "__all__"


class MerlinSerializer(NautobotModelSerializer):  # pylint: disable=too-many-ancestors
    """Merlin Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.Merlin
        fields = "__all__"
