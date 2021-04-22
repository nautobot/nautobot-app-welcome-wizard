"""Navigation menu for Merlin."""
from nautobot.extras.plugins import PluginMenuItem

plugin_items = [
    PluginMenuItem(
        link="plugins:merlin:manufacturer",
        link_text="Import Manufacturers",
        permissions=["merlin.view_manufacturerimport"],
    ),
    PluginMenuItem(
        link="plugins:merlin:devicetype",
        link_text="Import Device Types",
        permissions=["merlin.view_devicetypeimport"],
    ),
]

menu_items = tuple(plugin_items)
