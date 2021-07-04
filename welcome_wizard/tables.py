"""Tables for Welcome Wizard."""
import django_tables2 as tables

from django.conf import settings
from nautobot.utilities.tables import BaseTable, ToggleColumn
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport
from welcome_wizard.models.merlin import Merlin


MANUFACTURER_BUTTONS = """
<a href="{% url 'plugins:welcome_wizard:manufacturer_import' %}?pk={{ record.pk }}" class="btn btn-xs btn-info" title="Import Manufacturer">
    <i class="mdi mdi-database-import-outline" aria-hidden="true"></i>
</a>
"""

DEVICE_TYPE_BUTTONS = """
<a href="{% url 'plugins:welcome_wizard:devicetype_import' %}?pk={{ record.pk }}" class="btn btn-xs btn-info" title="Import Device Type">
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

DASHBOARD_LINK = """
<a href="{% url record.nautobot_list_link %}">{{ record.name }}</a>
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
        empty_text = "Add or Sync a Welcome Wizard Import Wizard GitRepository"
        if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library"):
            empty_text = "Adding data from GitRepository, please refresh"


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
        empty_text = "Add or Sync a Welcome Wizard Import Wizard GitRepository"
        if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library"):
            empty_text = "Adding data from GitRepository, please refresh"


class DashboardTable(BaseTable):  # pylint: disable=too-few-public-methods
    """Table for the Dashboard."""

    name = tables.TemplateColumn(verbose_name="Name", template_code=DASHBOARD_LINK)
    imports = tables.TemplateColumn(verbose_name="Actions", template_code=IMPORT_BUTTONS)
    completed_info = tables.TemplateColumn(verbose_name="Completed", template_code=COMPLETED_INFO)

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for Dashboard Table."""

        model = Merlin
        fields = ("name", "completed_info", "ignored", "imports")
        default_columns = ("name", "completed_info", "ignored", "imports")
