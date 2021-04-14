import string

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import ValidationError
from django.urls import reverse

from nautobot.core.models import BaseModel


def contains_whitespace(data):
    return any(char in data for char in string.whitespace)


class ManufacturerImport(BaseModel):
    """Store Manufacturers available for import."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:merlin:manufacturer")


class DeviceTypeImport(BaseModel):
    filename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(ManufacturerImport, on_delete=models.PROTECT, related_name="device_types")
    device_type_data = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("name",)
    
    def get_device_type_data(self):
        return self.device_type_data

    def clean(self):
        super().clean()

        if self.device_type_data and type(self.device_type_data) is not dict:
            raise ValidationError({"device_type_data": 'JSON data must be in object form. Example: {"foo": 123}'})
    
    def __str__(self):
        return self.name