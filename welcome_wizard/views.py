"""Views for Welcome Wizard."""

from django import forms
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import View
from nautobot.circuits.models import CircuitType, Provider
from nautobot.core.utils.permissions import get_permission_for_model
from nautobot.core.views import generic
from nautobot.core.views.mixins import ObjectPermissionRequiredMixin
from nautobot.dcim.models import DeviceType, Location, Manufacturer
from nautobot.extras.datasources import enqueue_pull_git_repository_and_refresh_data
from nautobot.extras.models import GitRepository, Job, JobResult, Role
from nautobot.ipam.models import RIR
from nautobot.virtualization.models import ClusterType

from welcome_wizard.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet
from welcome_wizard.forms import (
    DeviceTypeBulkImportForm,
    DeviceTypeImportFilterForm,
    ManufacturerBulkImportForm,
    ManufacturerImportFilterForm,
)
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport
from welcome_wizard.models.merlin import Merlin
from welcome_wizard.tables import DashboardTable, DeviceTypeImportTable, ManufacturerImportTable
from nautobot.apps.views import NautobotUIViewSet

from rest_framework.decorators import action
from nautobot.extras.models import Job, JobResult
from rest_framework import serializers


def check_sync(instance, request):
    """If Device Type Library is enabled and no data in queryset, run the sync."""
    print("Syncing Device Type Library ENTROU", instance.queryset.exists())
    print("Syncing Device Type Library", instance.queryset.exists())
    if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library") and not instance.queryset.exists():
        print("Syncing Device Type Library ENTROU")
        try:
            repo = GitRepository.objects.get(slug="devicetype_library")
            print("Syncing Device Type Library", repo, "ENTROU")
        except GitRepository.DoesNotExist:
            repo = GitRepository(
                name="Devicetype-library",
                slug="devicetype_library",
                remote_url="https://github.com/nautobot/devicetype-library.git",
                provided_contents=[
                    "welcome_wizard.import_wizard",
                ],
                branch="main",
            )
            repo.save()
            print("Syncing Device Type Library", repo, "SAIU")

        enqueue_pull_git_repository_and_refresh_data(repo, request.user)
        print("Syncing Device Type Library", repo, "SAIU 2")



class ManufacturerListView(NautobotUIViewSet):
    """List view for ManufacturerImport."""
    permission_required = "welcome_wizard.view_manufacturerimport"
    queryset = ManufacturerImport.objects.all()
    table_class = ManufacturerImportTable
    filterset_class = ManufacturerImportFilterSet
    filterset_form_class = ManufacturerImportFilterForm
    action_buttons = ()
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        check_sync(self, request)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get", "post"], url_path="import-wizard", url_name="import_wizard")
    def bulk_import(self, request):
        if not request.user.has_perm("dcim.add_manufacturer"):
            return HttpResponseForbidden()

        if request.method.lower() == "get":
            pk = request.GET.get("pk")
            if not pk:
                # volta pra lista padrão gerada pelo router
                return redirect("plugins:welcome_wizard:manufacturerimport_list")
            form = ManufacturerBulkImportForm(initial={"pk": [pk]})
            obj = self.queryset.model.objects.get(pk=pk)

            bulk_import_url = "plugins:welcome_wizard:manufacturer_import"
            return render(
                request,
                "welcome_wizard/import.html",
                {
                    "form": form,
                    "obj": obj,
                    "return_url": "plugins:welcome_wizard:manufacturers",
                    "bulk_import_url": bulk_import_url,
                    "breadcrumb_name": "Import Manufacturers",
                },
            )

        # POST
        print("entrou aqui 4?")
        form = ManufacturerBulkImportForm(request.POST)
        if form.is_valid():
            pk_list = request.POST.getlist("pk")
            onboarded = 0
            job = Job.objects.get(name="Welcome Wizard - Import Manufacturer")
            for obj in self.queryset.filter(pk__in=pk_list):
                JobResult.enqueue_job(job_model=job, user=request.user, manufacturer_name=obj.name)
                onboarded += 1
            messages.success(request, f"Onboarded {onboarded} objects.")
        return redirect("plugins:welcome_wizard:manufacturers")


class DeviceTypeListView(NautobotUIViewSet):
    """List view for DeviceTypeImport."""
    permission_required = "welcome_wizard.view_devicetypeimport"
    queryset = DeviceTypeImport.objects.select_related("manufacturer")
    table_class = DeviceTypeImportTable
    filterset_class = DeviceTypeImportFilterSet
    filterset_form_class = DeviceTypeImportFilterForm
    action_buttons = ()
    serializer_class = serializers.Serializer

    def list(self, request, *args, **kwargs):
        check_sync(self, request)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return redirect("plugins:welcome_wizard:devicetypeimport_list")

    @action(detail=False, methods=["get", "post"], url_path="import-wizard", url_name="import_wizard")
    def bulk_import(self, request):
        if not request.user.has_perm("dcim.add_devicetype"):
            return HttpResponseForbidden()

        if request.method.lower() == "get":
            pk = request.GET.get("pk")
            if not pk:
                return redirect("plugins:welcome_wizard:devicetypeimport_list")
            form = DeviceTypeBulkImportForm(initial={"pk": [pk]})
            obj = self.queryset.model.objects.get(pk=pk)
            bulk_import_url = "plugins:welcome_wizard:devicetype_import"
            return render(
                request,
                "welcome_wizard/import.html",
                {
                    "form": form,
                    "obj": obj,
                    "return_url": "plugins:welcome_wizard:devicetypes",
                    "bulk_import_url": bulk_import_url,
                    "breadcrumb_name": "Import Device Types",
                },
            )

        form = DeviceTypeBulkImportForm(request.POST)
        if form.is_valid():
            pk_list = request.POST.getlist("pk")
            onboarded = 0
            job = Job.objects.get(name="Welcome Wizard - Import Device Type")
            for obj in self.queryset.filter(pk__in=pk_list):
                JobResult.enqueue_job(job_model=job, user=request.user, filename=obj.filename)
                onboarded += 1
            messages.success(request, f"Onboarded {onboarded} objects.")
        return redirect("plugins:welcome_wizard:devicetypes")


class WelcomeWizardDashboard(NautobotUIViewSet):
    """Dashboard do Welcome Wizard."""
    action_buttons = ()
    permission_required = "welcome_wizard.view_merlin"
    queryset = Merlin.objects.all()
    table_class = DashboardTable
    filterset_class = None
    filterset_form_class = None
    serializer_class = serializers.Serializer

    @classmethod
    def check_data(cls):
        """Check data and update the Merlin database."""
        # Check the status of each of the Merlin Items
        # To not have a Merlin import set the `wizard_url` to an empty string `""` so that it will not be processed link
        # wise.
        for nautobot_object, var_name, list_url, new_url, wizard_url in [
            (Location, "Locations", "dcim:location_list", "dcim:location_add", ""),
            (
                Manufacturer,
                "Manufacturers",
                "dcim:manufacturer_list",
                "dcim:manufacturer_add",
                "plugins:welcome_wizard:manufacturer_import",
            ),
            (
                DeviceType,
                "Device Types",
                "dcim:devicetype_list",
                "dcim:devicetype_add",
                "plugins:welcome_wizard:devicetype_import",
            ),
            (
                Role,
                "Roles",
                "extras:role_list",
                "extras:role_add",
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
            Merlin.objects.update_or_create(
                name=var_name,
                defaults={
                    "completed": completed,
                    "ignored": False,
                    "nautobot_model": nautobot_object._meta.label,
                    "nautobot_add_link": new_url,
                    "merlin_link": wizard_url,
                    "nautobot_list_link": list_url,
                },
            )

    def get_extra_context(self, request, *args, **kwargs):
        # remove o filtro dinâmico
        context = super().get_extra_context(request, *args, **kwargs)
        context["dynamic_filter_form"] = None
        context["table_config_form"] = None
        context["search_form"] = None
        return context

    def list(self, request, *args, **kwargs):
        self.check_data()
        return super().list(request, *args, **kwargs)
