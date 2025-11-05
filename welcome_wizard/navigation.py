"""Menu items."""

from nautobot.apps.ui import NavigationIconChoices, NavigationWeightChoices, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:welcome_wizard:dashboard_list",
        name="Welcome Wizard Dashboard",
        permissions=["welcome_wizard.view_dashboard"],
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        icon=NavigationIconChoices.APPS,
        weight=NavigationWeightChoices.APPS,
        groups=(NavMenuGroup(name="Welcome Wizard", weight=600, items=tuple(items)),),
    ),
)
