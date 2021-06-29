"""Welcome Wizard Admin definition."""
from django.contrib import admin

from welcome_wizard.models.merlin import Merlin


@admin.register(Merlin)
class MerlinAdmin(admin.ModelAdmin):
    """Admin panel setup."""

    list_display = ("name", "completed", "ignored", "nautobot_model", "nautobot_add_link", "merlin_link")
