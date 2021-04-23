"""Tables for Merlin."""
import django_tables2 as tables

from nautobot.utilities.tables import BaseTable, ToggleColumn
from merlin.models.importer import DeviceTypeImport, ManufacturerImport
from merlin.models.merlin import Merlin


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

IMPORT_BUTTONS = """
<a href="{% url record.nautobot_add_link %}" class="btn btn-xs btn-success" title="Add"><i class="mdi mdi-plus-thick"></i></a>
{% if record.merlin_link %}
<a href="{% url record.merlin_link %}" class="btn btn-xs btn-info" title="Import"><i class="mdi mdi-wizard-hat"></i></a>
{% endif %}
"""

COMPLETED_INFO = """
{% if record.completed %}
<span class="mdi mdi-checkbox-marked-outline"></span>
{% else %}
<span class="mdi mdi-checkbox-blank-outline"></span>
{% endif %}
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


class DashboardTable(BaseTable):  # pylint: disable=too-few-public-methods
    """Table for the Dashboard."""

    name = tables.Column(accessor="name", verbose_name="Name")
    imports = tables.TemplateColumn(verbose_name="Actions", template_code=IMPORT_BUTTONS)
    completed_info = tables.TemplateColumn(verbose_name="Completed", template_code=COMPLETED_INFO)

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for Dashboard Table."""

        model = Merlin
        fields = ("name", "completed_info", "ignored", "imports")
        default_columns = ("name", "completed_info", "ignored", "imports")
