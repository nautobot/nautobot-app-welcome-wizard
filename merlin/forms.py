from django import forms
from merlin.models.importer import DeviceTypeImport, ManufacturerImport
from nautobot.utilities.forms import BootstrapMixin, DynamicModelMultipleChoiceField
from nautobot.extras.forms import CustomFieldFilterForm

class ManufacturerImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    model = ManufacturerImport
    q = forms.CharField(required=False, label="Search")

class DeviceTypeImportFilterForm(BootstrapMixin, CustomFieldFilterForm):
    model = DeviceTypeImport
    q = forms.CharField(required=False, label="Search")
    # manufacturer = DynamicModelMultipleChoiceField(
    #     queryset=ManufacturerImport.objects.all(), to_field_name="slug", required=False
    # )


class ManufacturerBulkImportForm(forms.Form):
    pk = forms.ModelMultipleChoiceField(queryset=ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput)


class DeviceTypeBulkImportForm(forms.Form):
    pk = forms.ModelMultipleChoiceField(queryset=DeviceTypeImport.objects.all(), widget=forms.MultipleHiddenInput)
