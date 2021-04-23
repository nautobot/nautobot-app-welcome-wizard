"""Views for Merlin."""

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.shortcuts import render, redirect
from nautobot.core.views import generic
from nautobot.dcim.models import DeviceType, Manufacturer
from nautobot.extras.datasources import enqueue_pull_git_repository_and_refresh_data
from nautobot.extras.models import JobResult, GitRepository
from nautobot.utilities.permissions import get_permission_for_model
from nautobot.utilities.views import ObjectPermissionRequiredMixin
from merlin.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet
from merlin.forms import (
    DeviceTypeImportFilterForm,
    DeviceTypeBulkImportForm,
    ManufacturerImportFilterForm,
    ManufacturerBulkImportForm,
)
from merlin.jobs import MerlinImportDeviceType, MerlinImportManufacturer
from merlin.models.importer import ManufacturerImport, DeviceTypeImport
from merlin.tables import ManufacturerTable, DeviceTypeTable


class ManufacturerListView(generic.ObjectListView):
    """Table of all Manufacturers discovered in the Git Repository."""

    permission_required = "merlin.view_manufacturerimport"
    table = ManufacturerTable
    queryset = ManufacturerImport.objects.all()
    action_buttons = None
    template_name = "merlin/manufacturer.html"
    filterset = ManufacturerImportFilterSet
    filterset_form = ManufacturerImportFilterForm

    def check_sync(self, request):
        """If Device Type Library is enabled and no data in queryset, run the sync."""
        if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library") and not self.queryset.exists():
            repo = GitRepository.objects.get(slug="devicetype_library")
            enqueue_pull_git_repository_and_refresh_data(repo, request)

    def get(self, request, *args, **kwargs):
        """Add Check Sync to Get."""
        self.check_sync(request=request)
        return super().get(request, *args, **kwargs)


class DeviceTypeListView(generic.ObjectListView):
    """Table of Device Types based on the Manufacturer."""

    permission_required = "merlin.view_devicetypeimport"
    table = DeviceTypeTable
    queryset = DeviceTypeImport.objects.prefetch_related("manufacturer")
    filterset = DeviceTypeImportFilterSet
    action_buttons = None
    template_name = "merlin/devicetype.html"
    filterset_form = DeviceTypeImportFilterForm

    def check_sync(self, request):
        """If Device Type Library is enabled and no data in queryset, run the sync."""
        if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library") and not self.queryset.exists():
            repo = GitRepository.objects.get(slug="devicetype_library")
            enqueue_pull_git_repository_and_refresh_data(repo, request)

    def get(self, request, *args, **kwargs):
        """Add Check Sync to Get."""
        self.check_sync(request=request)
        return super().get(request, *args, **kwargs)


class BulkImportView(View, ObjectPermissionRequiredMixin):
    """Generic Bulk Import View."""

    return_url = None
    model = None
    form = forms.Form
    bulk_import_url = None
    _permission_action = None

    def get_required_permission(self):
        """Return the specific permission necessary to perform the requested action on an object."""
        return get_permission_for_model(self.queryset.model, self._permission_action)

    def dispatch(self, request, *args, **kwargs):
        """Ensures User has permission to add."""
        # Following Nautobot style of adding self._permission_action inside the dispatch.
        self._permission_action = "add"  # pylint disable=attribute-defined-outside-init
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """Single Import Page."""
        # The user is expected to get here only by selecting the Import button from a list view.
        if not request.GET.get("pk"):
            return redirect(self.return_url)
        primarykey = request.GET["pk"]
        initial = {"pk": [primarykey]}

        obj = self.model.objects.get(pk=primarykey)
        form = self.form(initial)

        return render(
            request,
            "merlin/import.html",
            {"form": form, "obj": obj, "return_url": self.return_url, "bulk_import_url": self.bulk_import_url},
        )

    def post(self, request):
        """Import Processing."""
        if not self.has_permission():
            return HttpResponseForbidden()
        form = self.form(request.POST)
        if form.is_valid():
            pk_list = request.POST.getlist("pk")
            onboarded = []

            for obj in self.model.objects.filter(pk__in=pk_list):
                if self.model == ManufacturerImport:
                    data = {"manufacturer": obj.name}
                    job = MerlinImportManufacturer()
                    job.job_result = JobResult()
                    job.run(data, commit=True)
                    onboarded.append(obj.name)

                elif self.model == DeviceTypeImport:
                    job = MerlinImportDeviceType()
                    data = {"device_type": obj.filename}
                    job.job_result = JobResult()
                    job.run(data, commit=True)
                    onboarded.append(obj.name)

            # Currently treat everything as a success...
            messages.success(request, "Onboarded {} objects.".format(len(onboarded)))

        return redirect(self.return_url)


class ManufacturerBulkImportView(BulkImportView):
    """ManufacturerImport Bulk Import View."""

    model = ManufacturerImport
    form = ManufacturerBulkImportForm
    return_url = "plugins:merlin:manufacturer"
    bulk_import_url = "plugins:merlin:manufacturer_import"
    permission_required = "dcim.add_manufacturer"
    queryset = Manufacturer.objects.all()


class DeviceTypeBulkImportView(BulkImportView):
    """DeviceTypeImport Bulk Import View."""

    model = DeviceTypeImport
    form = DeviceTypeBulkImportForm
    return_url = "plugins:merlin:devicetype"
    bulk_import_url = "plugins:merlin:devicetype_import"
    permission_required = "dcim.add_devicetype"
    queryset = DeviceType.objects.prefetch_related("manufacturer")
