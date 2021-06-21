"""Navigation menu for Merlin."""
from nautobot.extras.plugins import PluginMenuItem

plugin_items = [
    PluginMenuItem(
        link="plugins:merlin:dashboard", link_text="Getting Started Wizard", permissions=["merlin.view_dashboard"]
    ),
]

menu_items = tuple(plugin_items)
