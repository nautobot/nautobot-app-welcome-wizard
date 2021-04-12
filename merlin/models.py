from django.db import models


class Merlin(models.Model):
    """Base model for Merlin Start.

    Args:
        models (model): Django model
    """

    all_completed = models.BooleanField(default=False)
    manufacturers = models.BooleanField(default=False)
    device_types = models.BooleanField(default=False)
    platforms = models.BooleanField(default=False)
    device_roles = models.BooleanField(default=False)
