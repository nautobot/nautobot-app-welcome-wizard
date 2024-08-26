"""Models definition for Welcome Wizard."""
from django.db import models

from nautobot.core.models import BaseModel


class Merlin(BaseModel):
    """Base model for Merlin Start.

    Keeping the Merlin name as a node to the original plugin name.

    Args:
        models (model): Django model
    """

    name = models.CharField(max_length=100, default="")
    completed = models.BooleanField(default=False)
    ignored = models.BooleanField(default=False)
    nautobot_model = models.CharField(verbose_name="Related Nautobot Model", default="", max_length=255)
    nautobot_add_link = models.CharField(verbose_name="Nautobot Model Add One Link", default="", max_length=255)
    merlin_link = models.CharField(max_length=200, default="", blank=True)
    nautobot_list_link = models.CharField(verbose_name="Nautobot Model List Link", default="", max_length=255)

    class Meta:
        """Meta definition."""

        verbose_name_plural = "merlin"

    def __str__(self):
        """Return name."""
        return self.name
