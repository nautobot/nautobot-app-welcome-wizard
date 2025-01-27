"""Menu items."""

from nautobot.apps.ui import NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:welcome_wizard:dashboard",
        name="Welcome Wizard Dashboard",
        permissions=["welcome_wizard.view_dashboard"],
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Welcome Wizard", items=tuple(items)),),
    ),
)
