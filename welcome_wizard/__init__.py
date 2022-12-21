"""Plugin declaration for Welcome Wizard."""

__version__ = "1.1.3"

from nautobot.extras.plugins import PluginConfig


class WelcomeWizardConfig(PluginConfig):
    """Plugin configuration for the welcome_wizard plugin."""

    name = "welcome_wizard"
    verbose_name = "Nautobot Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot's Getting Started Wizard."
    base_url = "welcome_wizard"
    required_settings = []
    min_version = "1.2.0"
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
