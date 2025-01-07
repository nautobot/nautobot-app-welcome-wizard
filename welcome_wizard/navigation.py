"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:welcome_wizard:manufacturerimport_list",
        name="Welcome Wizard",
        permissions=["welcome_wizard.view_manufacturerimport"],
        buttons=(
            NavMenuAddButton(
                link="plugins:welcome_wizard:manufacturerimport_add",
                permissions=["welcome_wizard.add_manufacturerimport"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Welcome Wizard", items=tuple(items)),),
    ),
)
