"""Navigation menu for Welcome Wizard."""

from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab

plugin_items = [
    NavMenuItem(
        link="plugins:welcome_wizard:dashboard",
        name="Welcome Wizard",
        permissions=["welcome_wizard.view_dashboard"],
    ),
]

menu_items = (
    NavMenuTab(
        name="Plugins",
        groups=(NavMenuGroup(name="Welcome Wizard", items=tuple(plugin_items)),),
    ),
)
