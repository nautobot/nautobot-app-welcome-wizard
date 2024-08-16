"""Home page banner for Welcome Wizard."""

from typing import Optional

from django.conf import settings
from django.urls import reverse
from django.utils.html import format_html
from nautobot.extras.choices import BannerClassChoices
from nautobot.extras.plugins import PluginBanner


def banner(context, *args, **kwargs) -> Optional[PluginBanner]:
    """
    Construct the Welcome Wizard Banner on the Home Page.

    These conditions must be met:
    - If User has permissions to the Welcome Wizard Dashboard (merlin)
    - On the Nautobot Home Page
    - enable_welcome_banner setting is True
    """
    required_permission = "welcome_wizard.view_merlin"

    if (
        context.request.path == "/"
        and context.request.user.is_authenticated
        and context.request.user.has_perms((required_permission,))
        and settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_welcome_banner")
    ):
        content = format_html(
            '<a href="{}">The Nautobot Welcome Wizard can help you get started with Nautobot!</a>',
            reverse("plugins:welcome_wizard:dashboard"),
        )
        return PluginBanner(content=content, banner_class=BannerClassChoices.CLASS_SUCCESS)
    return None
