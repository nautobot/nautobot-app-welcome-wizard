"""App declaration for welcome_wizard."""

from typing import Any

from nautobot.apps import NautobotAppConfig

# Needs to be resolved: This is due to a bug tracked by issue #86
__version__ = "2.0.0"


class WelcomeWizardConfig(NautobotAppConfig):
    """App configuration for the welcome_wizard app."""

    name = "welcome_wizard"
    verbose_name = "Nautobot Welcome Wizard"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot's Getting Started Wizard."
    base_url = "welcome_wizard"
<<<<<<< HEAD
    required_settings: list = []
    default_settings: dict[str, Any] = {
        # Add devicetype-library to Nautobot Git Repositories
        "enable_devicetype-library": True,
        "enable_welcome_banner": True,
        "manufacturer_transform_func": None,
        "manufacturer_map": {},
    }
    caching_config: dict = {}
    middleware = ["welcome_wizard.middleware.Prerequisites"]
    home_view_name = "plugins:welcome_wizard:dashboard_list"
=======
    required_settings = []
    default_settings = {}
>>>>>>> 4d1fa3d (Cookie updated by NetworkToCode Cookie Drift Manager Tool)
    docs_view_name = "plugins:welcome_wizard:docs"
    searchable_models = ["manufacturerimport", "devicetypeimport"]

    def ready(self):
        """Callback when this app is loaded."""
        super().ready()

        from nautobot.core.signals import nautobot_database_ready  # pylint: disable=import-outside-toplevel

        from .signals import nautobot_database_ready_callback  # pylint: disable=import-outside-toplevel

        nautobot_database_ready.connect(nautobot_database_ready_callback, sender=self)


config = WelcomeWizardConfig  # pylint:disable=invalid-name
