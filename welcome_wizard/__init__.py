"""App declaration for welcome_wizard."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotWelcomeWizardConfig(NautobotAppConfig):
    """App configuration for the welcome_wizard app."""

    name = "welcome_wizard"
    verbose_name = "Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot's Getting Started Wizard."
    base_url = "welcome_wizard"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotWelcomeWizardConfig  # pylint:disable=invalid-name
