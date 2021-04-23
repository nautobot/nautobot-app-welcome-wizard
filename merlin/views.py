"""Views for Merlin."""
from collections import OrderedDict

from django import forms
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.shortcuts import render, redirect
from nautobot.core.views import generic
from nautobot.dcim.models import Site, DeviceType, Manufacturer
from nautobot.dcim.models.devices import DeviceRole
from nautobot.circuits.models import CircuitType, Provider
from nautobot.ipam.models import RIR
from nautobot.virtualization.models import ClusterType
from nautobot.extras.models import JobResult
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
from merlin.models.merlin import Merlin
from merlin.tables import ManufacturerTable, DeviceTypeTable, DashboardTable


class ManufacturerListView(generic.ObjectListView):
    """Table of all Manufacturers discovered in the Git Repository."""

    permission_required = "merlin.view_manufacturerimport"
    table = ManufacturerTable
    queryset = ManufacturerImport.objects.all()
    action_buttons = None
    template_name = "merlin/manufacturer.html"
    filterset = ManufacturerImportFilterSet
    filterset_form = ManufacturerImportFilterForm


# class ManufacturerImportView(View):


class DeviceTypeListView(generic.ObjectListView):
    """Table of Device Types based on the Manufacturer."""

    permission_required = "merlin.view_devicetypeimport"
    table = DeviceTypeTable
    queryset = DeviceTypeImport.objects.prefetch_related("manufacturer")
    filterset = DeviceTypeImportFilterSet
    action_buttons = None
    template_name = "merlin/devicetype.html"
    filterset_form = DeviceTypeImportFilterForm


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


class MerlinDashboard(generic.ObjectListView):
    """Merlin dashboard view.

    Args:
        View (View): Django View
    """

    @classmethod
    def check_data(cls):
        """Check data and update the Merlin database."""
        dashboard_info = OrderedDict()
        # Check the status of each of the Merlin Items
        # To not have a Merlin import set the `wizard_url` to an empty string `""` so that it will not be processed link
        # wise.
        for nautobot_object, var_name, success_url, new_url, wizard_url in [
            (Site, "Sites", "dcim:site_list", "dcim:site_add", ""),
            (
                Manufacturer,
                "Manufacturers",
                "dcim:manufacturer_list",
                "dcim:manufacturer_add",
                "plugins:merlin:manufacturer_import",
            ),
            (
                DeviceType,
                "Device Types",
                "dcim:devicetype_list",
                "dcim:devicetype_add",
                "plugins:merlin:devicetype_import",
            ),
            (
                DeviceRole,
                "Device Roles",
                "dcim:devicerole_list",
                "dcim:devicerole_add",
                "",
            ),
            (
                CircuitType,
                "Circuit Types",
                "circuits:circuittype_list",
                "circuits:circuittype_add",
                "",
            ),
            (
                Provider,
                "Circuit Providers",
                "circuits:provider_list",
                "circuits:provider_add",
                "",
            ),
            (RIR, "RIRs", "ipam:rir_list", "ipam:rir_add", ""),
            (
                ClusterType,
                "VM Cluster Types",
                "virtualization:clustertype_list",
                "virtualization:clustertype_add",
                "",
            ),
        ]:
            completed = nautobot_object.objects.exists()
            if completed:
                dashboard_info[var_name] = {
                    "exists": True,
                    "next_url": success_url,
                    "nb_app": success_url.split(":")[0],
                }
            else:
                dashboard_info[var_name] = {
                    "exists": False,
                    "next_url": new_url,
                    "nb_app": new_url.split(":")[0],
                    "wizard_url": wizard_url,
                }
            try:
                merlin_id = Merlin.objects.get(name=var_name)
                Merlin.objects.filter(name=var_name).update(completed=completed)
            except Merlin.DoesNotExist:
                merlin_id = None

            if merlin_id is None:
                Merlin.objects.create(
                    name=var_name,
                    completed=completed,
                    ignored=False,
                    nautobot_model=nautobot_object,
                    nautobot_add_link=new_url,
                    merlin_link=wizard_url,
                )

    def get(self, request, *args, **kwargs):
        """Get request."""
        self.check_data()
        return super().get(request, *args, **kwargs)

    permission_required = "merlin.view_merlin"
    queryset = Merlin.objects.all()
    template_name = "merlin/dashboard.html"
    table = DashboardTable
