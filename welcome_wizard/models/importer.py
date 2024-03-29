"""Models definition for Welcome Wizard Importer."""

from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import ValidationError
from django.db import models
from django.urls import reverse
from nautobot.core.models import BaseModel


class ManufacturerImport(BaseModel):
    """Store Manufacturers available for import."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta for ManufacturerImport."""

        ordering = ("name",)

    def __str__(self):
        """Return name for string method."""
        return self.name

    def get_absolute_url(self, api=False):
        """Return the absolute url for ManufacturerImport."""
        return reverse("plugins:welcome_wizard:manufacturer", kwargs={"pk": self.pk})


class DeviceTypeImport(BaseModel):
    """Store Device Types available for import."""

    filename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(ManufacturerImport, on_delete=models.PROTECT, related_name="device_types")
    device_type_data = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        null=True,
    )

    class Meta:
        """Meta for DeviceTypeImport."""

        ordering = ("name",)

    def clean(self):
        """Validates device_type_data exists and is a dictionary."""
        super().clean()

        if self.device_type_data and not isinstance(self.device_type_data, dict):
            raise ValidationError({"device_type_data": 'JSON data must be in object form. Example: {"foo": 123}'})

    def __str__(self):
        """Return name for string method."""
        return self.name

    def get_absolute_url(self, api=False):
        """Return the absolute url for DeviceTypeImport."""
        return reverse("plugins:welcome_wizard:devicetype", kwargs={"pk": self.pk})
