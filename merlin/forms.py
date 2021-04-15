"""Forms for Merlin."""

from django import forms
from nautobot.utilities.forms import BootstrapMixin
from nautobot.extras.forms import CustomFieldFilterForm
from merlin.models.importer import DeviceTypeImport, ManufacturerImport


class ManufacturerImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    """Filter form for Manufacturer."""

    model = ManufacturerImport
    q = forms.CharField(required=False, label="Search")


class DeviceTypeImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    """Filter form for Device Type."""

    model = DeviceTypeImport
    q = forms.CharField(required=False, label="Search")
    # TODO to be added once we use Nautobot develop branch or once 1.0.0 of Nuatobot is released.
    # manufacturer = DynamicModelMultipleChoiceField(
    #     queryset=ManufacturerImport.objects.all(), to_field_name="slug", required=False
    # )


class ManufacturerBulkImportForm(forms.Form):
    """Bulk Import Form for Manufacturer."""

    pk = forms.ModelMultipleChoiceField(queryset=ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput)


class DeviceTypeBulkImportForm(forms.Form):
    """Bulk Import Form for Device Type."""

    pk = forms.ModelMultipleChoiceField(queryset=DeviceTypeImport.objects.all(), widget=forms.MultipleHiddenInput)
