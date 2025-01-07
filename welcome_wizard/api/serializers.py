"""API serializers for welcome_wizard."""

from nautobot.apps.api import NautobotModelSerializer, TaggedModelSerializerMixin

from welcome_wizard import models


class ManufacturerImportSerializer(NautobotModelSerializer, TaggedModelSerializerMixin):  # pylint: disable=too-many-ancestors
    """ManufacturerImport Serializer."""

    class Meta:
        """Meta attributes."""

        model = models.ManufacturerImport
        fields = "__all__"

        # Option for disabling write for certain fields:
        # read_only_fields = []
