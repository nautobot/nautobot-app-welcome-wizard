"""Forms for Welcome Wizard."""

from django import forms
from nautobot.apps.forms import DynamicModelMultipleChoiceField
from nautobot.core.forms import BootstrapMixin
from nautobot.extras.forms import CustomFieldFilterForm

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    """Filter form for Manufacturer."""

    model = ManufacturerImport
    q = forms.CharField(required=False, label="Search")


class DeviceTypeImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    """Filter form for Device Type."""

    model = DeviceTypeImport
    q = forms.CharField(required=False, label="Search")
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=ManufacturerImport.objects.all(), to_field_name="name", required=False
    )


class ManufacturerBulkImportForm(BootstrapMixin, forms.Form):
    """Bulk Import Form for Manufacturer."""

    pk = forms.ModelMultipleChoiceField(queryset=ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput)


class DeviceTypeBulkImportForm(BootstrapMixin, forms.Form):
    """Bulk Import Form for Device Type."""

    pk = forms.ModelMultipleChoiceField(queryset=DeviceTypeImport.objects.all(), widget=forms.MultipleHiddenInput)
