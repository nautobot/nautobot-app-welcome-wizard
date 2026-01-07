"""Views for Welcome Wizard."""

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from nautobot.apps.ui import BaseBreadcrumbItem, Breadcrumbs, ModelBreadcrumbItem, ViewNameBreadcrumbItem
from nautobot.apps.views import (
    NautobotUIViewSet,
    ObjectChangeLogViewMixin,
    ObjectListViewMixin,
)
from nautobot.circuits.models import CircuitType, Provider
from nautobot.dcim.models import DeviceType, Location, Manufacturer
from nautobot.extras.datasources import enqueue_pull_git_repository_and_refresh_data
from nautobot.extras.models import GitRepository, Job, JobResult, Role
from nautobot.ipam.models import RIR
from nautobot.virtualization.models import ClusterType
from rest_framework.decorators import action

from welcome_wizard.api import serializers
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

# DEPRECATION NOTICE:
# Merlin's *_link fields (nautobot_add_link, nautobot_list_link, merlin_link) are deprecated.
# Do NOT introduce new code that reads/writes these fields. New code must derive URLs
# from `Merlin.nautobot_model`, not from DB-stored links.


def check_sync(instance, request):
    """If Device Type Library is enabled and no data in queryset, run the sync."""
    if settings.PLUGINS_CONFIG["welcome_wizard"].get("enable_devicetype-library") and not instance.queryset.exists():
        try:
            repo = GitRepository.objects.get(slug="devicetype_library")
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

        enqueue_pull_git_repository_and_refresh_data(repo, request.user)


class ManufacturerImportUIViewSet(ObjectListViewMixin, ObjectChangeLogViewMixin):  # pylint: disable=abstract-method
    """List view for ManufacturerImport."""

    permission_required = "welcome_wizard.view_manufacturerimport"
    queryset = ManufacturerImport.objects.all()
    table_class = ManufacturerImportTable
    filterset_class = ManufacturerImportFilterSet
    filterset_form_class = ManufacturerImportFilterForm
    action_buttons = ()
    serializer_class = serializers.ManufacturerImportSerializer
    breadcrumbs = Breadcrumbs(
        items={
            "list": [
                BaseBreadcrumbItem(label="Welcome Wizard"),
                ViewNameBreadcrumbItem(view_name="plugins:welcome_wizard:dashboard_list", label="Dashboard"),
                ModelBreadcrumbItem(model=ManufacturerImport),
            ],
        }
    )

    def list(self, request, *args, **kwargs):
        """Return the list view for ManufacturerImport objects."""
        check_sync(self, request)
        return super().list(request, *args, **kwargs)

    def get_required_permission(self):
        """Return the required permission for the current action."""
        view_action = self.get_action()
        if view_action == "import_wizard":
            return [
                *self.get_permissions_for_model(Manufacturer, ["add"]),
            ]
        return super().get_required_permission()

    @action(detail=False, methods=["get", "post"], url_path="import-wizard", url_name="import_wizard")
    def import_wizard(self, request):
        """Handle bulk import of ManufacturerImport objects."""
        if request.method.lower() == "get":
            pk = request.GET.get("pk")
            if not pk:
                return redirect("plugins:welcome_wizard:manufacturerimport_list")
            form = ManufacturerBulkImportForm(initial={"pk": [pk]})
            obj = self.queryset.model.objects.get(pk=pk)

            bulk_import_url = "plugins:welcome_wizard:manufacturerimport_import_wizard"
            return render(
                request,
                "welcome_wizard/import.html",
                {
                    "form": form,
                    "obj": obj,
                    "return_url": "plugins:welcome_wizard:manufacturerimport_list",
                    "bulk_import_url": bulk_import_url,
                    "breadcrumb_name": "Import Manufacturers",
                },
            )

        # POST
        form = ManufacturerBulkImportForm(request.POST)
        if form.is_valid():
            pk_list = request.POST.getlist("pk")
            objects_to_onboard = self.queryset.filter(pk__in=pk_list)
            job = Job.objects.get(name="Welcome Wizard - Import Manufacturer")
            for obj in objects_to_onboard:
                JobResult.enqueue_job(job_model=job, user=request.user, manufacturer_name=obj.name)
            messages.success(request, f"Onboarded {objects_to_onboard.count()} objects.")
        return redirect("plugins:welcome_wizard:manufacturerimport_list")


class DeviceTypeImportUIViewSet(
    ObjectListViewMixin,
    ObjectChangeLogViewMixin,
):  # pylint: disable=abstract-method
    """List view for DeviceTypeImport."""

    queryset = DeviceTypeImport.objects.select_related("manufacturer")
    table_class = DeviceTypeImportTable
    filterset_class = DeviceTypeImportFilterSet
    filterset_form_class = DeviceTypeImportFilterForm
    action_buttons = ()
    serializer_class = serializers.DeviceTypeImportSerializer
    breadcrumbs = Breadcrumbs(
        items={
            "list": [
                BaseBreadcrumbItem(label="Welcome Wizard"),
                ViewNameBreadcrumbItem(view_name="plugins:welcome_wizard:dashboard_list", label="Dashboard"),
                ModelBreadcrumbItem(model=DeviceTypeImport),
            ],
        }
    )

    def get_required_permission(self):
        """Return the required permission for the current action."""
        view_action = self.get_action()
        if view_action == "import_wizard":
            return [
                *self.get_permissions_for_model(DeviceType, ["add"]),
            ]
        return super().get_required_permission()

    def list(self, request, *args, **kwargs):
        """Return the list view for DeviceTypeImport objects."""
        check_sync(self, request)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["get", "post"], url_path="import-wizard", url_name="import_wizard")
    def import_wizard(self, request):
        """Handle bulk import of DeviceTypeImport objects."""
        if request.method.lower() == "get":
            pk = request.GET.get("pk")
            if not pk:
                return redirect("plugins:welcome_wizard:devicetypeimport_list")
            form = DeviceTypeBulkImportForm(initial={"pk": [pk]})
            obj = self.queryset.model.objects.get(pk=pk)
            bulk_import_url = "plugins:welcome_wizard:devicetypeimport_import_wizard"
            return render(
                request,
                "welcome_wizard/import.html",
                {
                    "form": form,
                    "obj": obj,
                    "return_url": "plugins:welcome_wizard:devicetypeimport_list",
                    "bulk_import_url": bulk_import_url,
                    "breadcrumb_name": "Import Device Types",
                },
            )

        form = DeviceTypeBulkImportForm(request.POST)
        if form.is_valid():
            pk_list = request.POST.getlist("pk")
            objects_to_onboard = self.queryset.filter(pk__in=pk_list)
            job = Job.objects.get(name="Welcome Wizard - Import Device Type")
            for obj in objects_to_onboard:
                JobResult.enqueue_job(job_model=job, user=request.user, filename=obj.filename)
            messages.success(request, f"Onboarded {objects_to_onboard.count()} objects.")
        return redirect("plugins:welcome_wizard:devicetypeimport_list")


class MerlinUIViewSet(NautobotUIViewSet):
    """Welcome Wizard Dashboard."""

    action_buttons = ()
    permission_required = "welcome_wizard.view_merlin"
    queryset = Merlin.objects.all()
    table_class = DashboardTable
    breadcrumbs = Breadcrumbs(
        items={
            "list": [
                BaseBreadcrumbItem(label="Welcome Wizard"),
                ViewNameBreadcrumbItem(view_name="plugins:welcome_wizard:dashboard_list", label="Dashboard"),
            ],
        }
    )

    @classmethod
    def check_data(cls):
        """Check data and update the Merlin database."""
        # Check the status of each of the Merlin Items
        # To not have a Merlin import set the `wizard_url` to an empty string `""` so that it will not be processed link
        # wise.
        for model, name, nautobot_list_link, nautobot_add_link, merlin_link in [
            (Location, "Locations", "dcim:location_list", "dcim:location_add", ""),
            (
                Manufacturer,
                "Manufacturers",
                "dcim:manufacturer_list",
                "dcim:manufacturer_add",
                "plugins:welcome_wizard:manufacturerimport_import_wizard",
            ),
            (
                DeviceType,
                "Device Types",
                "dcim:devicetype_list",
                "dcim:devicetype_add",
                "plugins:welcome_wizard:devicetypeimport_import_wizard",
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
            completed = model.objects.exists()
            Merlin.objects.update_or_create(
                name=name,
                defaults={
                    "completed": completed,
                    "ignored": False,
                    "nautobot_model": model._meta.label,
                    "nautobot_add_link": nautobot_add_link,
                    "merlin_link": merlin_link,
                    "nautobot_list_link": nautobot_list_link,
                },
            )

    def get_extra_context(self, request, *args, **kwargs):
        """Customize context by removing dynamic filters and search forms."""
        context = super().get_extra_context(request, *args, **kwargs)
        context["dynamic_filter_form"] = None
        context["table_config_form"] = None
        context["search_form"] = None
        return context

    def list(self, request, *args, **kwargs):
        """Render the Welcome Wizard dashboard with updated data."""
        self.check_data()
        return super().list(request, *args, **kwargs)
