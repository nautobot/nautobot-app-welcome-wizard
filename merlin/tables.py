"""Tables for Merlin."""
import django_tables2 as tables

from django.conf import settings
from nautobot.utilities.tables import BaseTable, ToggleColumn
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


MANUFACTURER_BUTTONS = """
<a href="{% url 'plugins:merlin:manufacturer_import' %}?pk={{ record.pk }}" class="btn btn-xs btn-info" title="Import Manufacturer">
    <i class="mdi mdi-database-import-outline" aria-hidden="true"></i>
</a>
"""

DEVICE_TYPE_BUTTONS = """
<a href="{% url 'plugins:merlin:devicetype_import' %}?pk={{ record.pk }}" class="btn btn-xs btn-info" title="Import Device Type">
    <i class="mdi mdi-database-import-outline" aria-hidden="true"></i>
</a>
"""


class ManufacturerTable(BaseTable):
    """Table to show the ManufactureImport List."""

    pk = ToggleColumn()
    name = tables.Column(accessor="name", verbose_name="Name")
    actions = tables.TemplateColumn(MANUFACTURER_BUTTONS)

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for ManufacturerImport Table."""

        model = ManufacturerImport
        fields = ("pk", "name", "actions")
        default_columns = ("pk", "name", "actions")
        if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library"):
            empty_text = "Adding data from GitRepository, please refresh"
        else:
            empty_text = "Add or Sync a Merlin Import Wizard GitRepository"


class DeviceTypeTable(BaseTable):
    """Table to show the DeviceTypeImport List."""

    pk = ToggleColumn()
    name = tables.Column(accessor="name", verbose_name="Name")
    manufacturer = tables.Column(accessor="manufacturer", verbose_name="Manufacturer")
    actions = tables.TemplateColumn(DEVICE_TYPE_BUTTONS)

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for DeviceTypeImport Table."""

        model = DeviceTypeImport
        fields = ("pk", "name", "manufacturer", "actions")
        default_columns = ("pk", "name", "manufacturer", "actions")
        empty_text = "Add or Sync a Merlin Import Wizard GitRepository"
