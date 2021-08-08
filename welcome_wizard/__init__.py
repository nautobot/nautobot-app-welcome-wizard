"""Plugin declaration for Welcome Wizard."""

__version__ = "1.0.1"

from django.db.models.signals import post_migrate
from nautobot.extras.plugins import PluginConfig

from welcome_wizard.signals import welcome_wizard_devicetype


class WelcomeWizardConfig(PluginConfig):
    """Plugin configuration for the welcome_wizard plugin."""

    name = "welcome_wizard"
    verbose_name = "Nautobot Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot's Getting Started Wizard."
    base_url = "welcome_wizard"
    required_settings = []
    min_version = "1.0.0b4"
    default_settings = {
        # Add devicetype-library to Nautobot Git Repositories
        "enable_devicetype-library": True,
    }
    caching_config = {}
    middleware = ["welcome_wizard.middleware.Prerequisites"]

    def ready(self):
        """If enable_devicetype-library is true, create the Git Repository."""
        super().ready()

        post_migrate.connect(welcome_wizard_devicetype, sender=self)


config = WelcomeWizardConfig  # pylint:disable=invalid-name
