"""Welcome Wizard Admin definition."""

from django.contrib import admin

from welcome_wizard.models.importer import ManufacturerImport, DeviceTypeImport
from welcome_wizard.models.merlin import Merlin


@admin.register(Merlin)
class MerlinAdmin(admin.ModelAdmin):
    """Admin panel setup."""

    list_display = ("name", "completed", "ignored", "nautobot_model", "nautobot_add_link", "merlin_link")


@admin.register(ManufacturerImport)
class ManufacturerImportAdmin(admin.ModelAdmin):
    """Admin panel setup."""

    list_display = ("name",)


@admin.register(DeviceTypeImport)
class DeviceTypeImportAdmin(admin.ModelAdmin):
    """Admin panel setup."""

    list_display = ("name", "filename", "manufacturer")
    list_filter = ("manufacturer",)
    search_fields = ("name",)
    ordering = ("manufacturer", "name")
