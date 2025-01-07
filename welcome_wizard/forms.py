"""Forms for welcome_wizard."""

from django import forms
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin

from welcome_wizard import models


class ManufacturerImportForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """ManufacturerImport creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ManufacturerImport
        fields = [
            "name",
            "description",
        ]


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
        help_text="Search within Name or Slug.",
    )
    name = forms.CharField(required=False, label="Name")
