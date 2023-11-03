"""Plugin declaration for Welcome Wizard."""
from importlib import metadata

from django.conf import settings
from nautobot.extras.plugins import NautobotAppConfig

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import PluginConfig


class WelcomeWizardConfig(NautobotAppConfig):
    """Plugin configuration for the welcome_wizard plugin."""

    name = "welcome_wizard"
    verbose_name = "Nautobot Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot's Getting Started Wizard."
    base_url = "welcome_wizard"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {
        # Add devicetype-library to Nautobot Git Repositories
        "enable_devicetype-library": True,
        "enable_welcome_banner": True,
    }
    caching_config = {}
    middleware = ["welcome_wizard.middleware.Prerequisites"]
    home_view_name = "plugins:welcome_wizard:dashboard"
    docs_view_name = "plugins:welcome_wizard:docs"


config = WelcomeWizardConfig  # pylint:disable=invalid-name
