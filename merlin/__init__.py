"""Plugin declaration for merlin."""

__version__ = "0.1.0"

from nautobot.extras.plugins import PluginConfig


class MerlinConfig(PluginConfig):
    """Plugin configuration for the merlin plugin."""

    name = "merlin"
    verbose_name = "Merlin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Merlin."
    base_url = "merlin"
    required_settings = []
    min_version = "1.0.0b1"
    max_version = "1.0.0b2"
    default_settings = {}
    caching_config = {}
    middleware = ["merlin.middleware.Prerequisites"]


config = MerlinConfig  # pylint:disable=invalid-name
