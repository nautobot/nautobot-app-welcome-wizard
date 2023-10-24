"""Plugin declaration for welcome_wizard."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import NautobotAppConfig


class NautobotWelcomeWizardConfig(NautobotAppConfig):
    """Plugin configuration for the welcome_wizard plugin."""

    name = "welcome_wizard"
    verbose_name = "Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Welcome Wizard."
    base_url = "nautobot-welcome-wizard"
    required_settings = []
    min_version = "1.5.0"
    max_version = "1.9999"
    default_settings = {}
    caching_config = {}


config = NautobotWelcomeWizardConfig  # pylint:disable=invalid-name
