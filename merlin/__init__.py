"""Plugin declaration for merlin."""

__version__ = "0.1.0"

from django.db.models.signals import post_migrate
from nautobot.extras.plugins import PluginConfig

from merlin.signals import merlin_devicetype


class MerlinConfig(PluginConfig):
    """Plugin configuration for the merlin plugin."""

    name = "merlin"
    verbose_name = "Merlin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Merlin."
    base_url = "merlin"
    required_settings = []
    min_version = "1.0.0b4"
    default_settings = {
        # Add devicetype-library to Nautobot Git Repositories
        "enable_devicetype-library": True,
    }
    caching_config = {}
    middleware = ["merlin.middleware.Prerequisites"]

    def ready(self):
        """If enable_devicetype-library is true, create the Git Repository."""
        super().ready()

        post_migrate.connect(merlin_devicetype, sender=self)


config = MerlinConfig  # pylint:disable=invalid-name
