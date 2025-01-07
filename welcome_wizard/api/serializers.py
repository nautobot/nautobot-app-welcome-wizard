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
