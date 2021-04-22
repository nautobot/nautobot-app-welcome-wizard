"""Models definition for Merlin."""
from django.db import models


class Merlin(models.Model):
    """Base model for Merlin Start.

    Args:
        models (model): Django model
    """

    name = models.CharField()
    completed = models.BooleanField(default=False)
    ignored = models.BooleanField(default=False)
    nautobot_model = models.CharField(verbose_name="Related Nautobot Model", default="")
    nautobot_add_link = models.CharField(verbose_name="Nautobot Add One Link")
    merlin_link = models.CharField()

    def __str__(self):
        """Return name."""
        return self.name
