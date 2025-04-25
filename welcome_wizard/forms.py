"""Forms for welcome_wizard."""

from django import forms
from nautobot.apps.forms import BootstrapMixin, DynamicModelMultipleChoiceField, NautobotFilterForm

from welcome_wizard import models


class ManufacturerImportForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """ManufacturerImport creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ManufacturerImport
        fields = "__all__"


class ManufacturerImportBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """ManufacturerImport bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ManufacturerImportFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.ManufacturerImport
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name.",
    )
    name = forms.CharField(required=False, label="Name")


class DeviceTypeImportFilterForm(NautobotFilterForm):  # pylint: disable=too-many-ancestors
    """Filter form to filter searches."""

    model = models.DeviceTypeImport
    field_order = ["q", "manufacturer"]

    q = forms.CharField(
        required=False,
        label="Search",
    )
    manufacturer = DynamicModelMultipleChoiceField(
        queryset=models.ManufacturerImport.objects.all(),
        to_field_name="name",
        required=False,
        label="Manufacturer",
    )


class ManufacturerBulkImportForm(BootstrapMixin, forms.Form):
    """Bulk Import Form for Manufacturer."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput
    )


class DeviceTypeBulkImportForm(BootstrapMixin, forms.Form):
    """Bulk Import Form for Device Type."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.DeviceTypeImport.objects.all(), widget=forms.MultipleHiddenInput
    )
