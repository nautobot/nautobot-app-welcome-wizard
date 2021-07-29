"""Navigation menu for Welcome Wizard."""
from nautobot.extras.plugins import PluginMenuItem

plugin_items = [
    PluginMenuItem(
        link="plugins:welcome_wizard:dashboard",
        link_text="Welcome Wizard",
        permissions=["welcome_wizard.view_dashboard"],
    ),
]

menu_items = tuple(plugin_items)
