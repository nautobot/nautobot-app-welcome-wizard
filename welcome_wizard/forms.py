"""Forms for welcome_wizard."""

from django import forms
<<<<<<< HEAD
from nautobot.apps.forms import BootstrapMixin, DynamicModelMultipleChoiceField, NautobotFilterForm
=======
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin
>>>>>>> 8deaff5 (Cookie updated by NetworkToCode Cookie Drift Manager Tool)

from welcome_wizard import models


<<<<<<< HEAD
class ManufacturerImportFilterForm(NautobotFilterForm):  # pylint: disable=too-many-ancestors
=======
class ManufacturerImportForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """ManufacturerImport creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ManufacturerImport
        fields = "__all__"


class ManufacturerImportBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """ManufacturerImport bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ManufacturerImport.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False, max_length=CHARFIELD_MAX_LENGTH)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ManufacturerImportFilterForm(NautobotFilterForm):
>>>>>>> 8deaff5 (Cookie updated by NetworkToCode Cookie Drift Manager Tool)
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
