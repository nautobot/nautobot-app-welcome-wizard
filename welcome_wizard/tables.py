"""Tables for welcome_wizard."""

import django_tables2 as tables
from django.conf import settings
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn

from welcome_wizard import models

MANUFACTURER_BUTTONS = """
<li>
    <a href="{% url 'plugins:welcome_wizard:manufacturerimport_import_wizard' %}?pk={{ record.pk }}" class="dropdown-item text-primary" title="Import Manufacturer">
        <span class="mdi mdi-database-import-outline" aria-hidden="true"></span>
        Import Manufacturer
    </a>
</li>
"""

DEVICE_TYPE_BUTTONS = """
<li>
    <a href="{% url 'plugins:welcome_wizard:devicetypeimport_import_wizard' %}?pk={{ record.pk }}" class="dropdown-item text-primary" title="Import Device Type">
        <span class="mdi mdi-database-import-outline" aria-hidden="true"></span>
        Import Device Types
    </a>
</li>
"""

IMPORT_BUTTONS = """
<a href="{% url record.nautobot_add_link %}" class="btn btn-xs btn-success" title="Add"><i class="mdi mdi-plus-thick"></i></a>
{% if record.nautobot_model == "dcim.Manufacturer" %}
<a href="{% url 'plugins:welcome_wizard:manufacturerimport_import_wizard' %}" class="btn btn-xs btn-info" title="Import"><i class="mdi mdi-wizard-hat"></i></a>
{% elif record.nautobot_model == "dcim.DeviceType" %}
<a href="{% url 'plugins:welcome_wizard:devicetypeimport_import_wizard' %}" class="btn btn-xs btn-info" title="Import"><i class="mdi mdi-wizard-hat"></i></a>
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


class ManufacturerImportTable(BaseTable):
    """Table to show the ManufactureImport List."""

    pk = ToggleColumn()
    name = tables.Column(accessor="name", verbose_name="Name")
    actions = ButtonsColumn(
        model=models.ManufacturerImport,
        prepend_template=MANUFACTURER_BUTTONS,
        buttons=[
            "",
        ],
    )

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for ManufacturerImport Table."""

        model = models.ManufacturerImport
        fields = ("pk", "name", "actions")
        default_columns = ("pk", "name", "actions")
        empty_text = "Add or Sync a Welcome Wizard Import Wizard GitRepository"
        if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library"):
            empty_text = "Adding data from GitRepository, please refresh"


class DeviceTypeImportTable(BaseTable):
    """Table to show the DeviceTypeImport List."""

    pk = ToggleColumn()
    name = tables.Column(accessor="name", verbose_name="Name")
    manufacturer = tables.Column(accessor="manufacturer", verbose_name="Manufacturer")
    actions = ButtonsColumn(
        model=models.DeviceTypeImport,
        prepend_template=DEVICE_TYPE_BUTTONS,
        buttons=[
            "",
        ],
    )

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for DeviceTypeImport Table."""

        model = models.DeviceTypeImport
        fields = ("pk", "name", "manufacturer", "actions")
        default_columns = ("pk", "name", "manufacturer", "actions")
        empty_text = "Add or Sync a Welcome Wizard Import Wizard GitRepository"
        if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library"):
            empty_text = "Adding data from GitRepository, please refresh"


class DashboardTable(BaseTable):  # pylint: disable=too-few-public-methods, nb-sub-class-name
    """Table for the Dashboard."""

    name = tables.TemplateColumn(verbose_name="Name", template_code=DASHBOARD_LINK)
    imports = tables.TemplateColumn(verbose_name="Actions", template_code=IMPORT_BUTTONS)
    completed_info = tables.TemplateColumn(verbose_name="Completed", template_code=COMPLETED_INFO)

    class Meta(BaseTable.Meta):  # pylint: disable=too-few-public-methods
        """Meta for Dashboard Table."""

        model = models.Merlin
        fields = ("name", "completed_info", "ignored", "imports")
        default_columns = ("name", "completed_info", "ignored", "imports")
