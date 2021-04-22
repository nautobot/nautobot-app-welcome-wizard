from django.contrib import admin

from merlin.models.merlin import Merlin


@admin.register(Merlin)
class MerlinAdmin(admin.ModelAdmin):
    list_display = ("name", "completed", "ignored", "nautobot_model", "nautobot_add_link", "merlin_link")
