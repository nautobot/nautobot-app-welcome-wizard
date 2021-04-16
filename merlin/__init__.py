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
    min_version = "1.0.0b4"
    default_settings = {
        # Add devicetype-library to Nautobot Git Repositories
        "enable_devicetype-library": False,
    }
    caching_config = {}

    def ready(self):
        """If enable_devicetype-library is true, create the Git Repository."""
        super().ready()
        # pylint: disable=import-outside-toplevel
        from django.conf import settings

        if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library"):
            from nautobot.extras.models import GitRepository

            try:
                repo = GitRepository.objects.get(name="Devicetype-library")
            except GitRepository.DoesNotExist:
                repo = GitRepository(
                    name="Devicetype-library",
                    slug="devicetype_library",
                    remote_url="https://github.com/netbox-community/devicetype-library.git",
                    provided_contents=["merlin.device_type_importer",],
                    branch="master",
                )
                repo.save(trigger_resync=False)


config = MerlinConfig  # pylint:disable=invalid-name
