"""Views for Merlin."""
import logging

from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from nautobot.core.views import generic
from nautobot.extras.models import JobResult
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


logger = logging.getLogger(__name__)


class ManufacturerListView(generic.ObjectListView):
    """Table of all Manufacturers discovered in the Git Repository."""

    table = ManufacturerTable
    queryset = ManufacturerImport.objects.all()
    action_buttons = None
    template_name = "merlin/manufacturer.html"
    filterset = ManufacturerImportFilterSet
    filterset_form = ManufacturerImportFilterForm


# class ManufacturerImportView(View):


class DeviceTypeListView(generic.ObjectListView):
    """Table of Device Types based on the Manufacturer."""

    table = DeviceTypeTable
    queryset = DeviceTypeImport.objects.prefetch_related("manufacturer")
    filterset = DeviceTypeImportFilterSet
    action_buttons = None
    template_name = "merlin/devicetype.html"
    filterset_form = DeviceTypeImportFilterForm


class BulkImportView(View):
    """Generic Bulk Import View."""

    def __init__(self, model, form, return_url, bulk_import_url):
        """Initializes the required settings for the Bulk Import View.

        Args:
            model (django_model): Model to be used for the Import.
            form (django_form): Form to accept data from the user.
            return_url (str): Reverse compatible URL to return user to upon form submission.
            bulk_import_url (str): Reverse compatible URL for the form submission.
        """
        super().__init__()
        self.model = model
        self.form = form
        self.return_url = return_url
        self.bulk_import_url = bulk_import_url

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
        if request.method != "POST":
            return redirect(self.return_url)
        form = self.form(request.POST)
        if form.is_valid():
            logger.debug("Form validation was successful")
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

    # I am not sure how to do the cool class declarations like the rest of Nautobot,
    # so here is a boring init.
    def __init__(self, model=model, form=form, return_url=return_url, bulk_import_url=bulk_import_url):
        """Initialize ManufacturerImport Bulk Import View."""
        BulkImportView.__init__(self, model, form, return_url, bulk_import_url)


class DeviceTypeBulkImportView(BulkImportView):
    """DeviceTypeImport Bulk Import View."""

    model = DeviceTypeImport
    form = DeviceTypeBulkImportForm
    return_url = "plugins:merlin:devicetype"
    bulk_import_url = "plugins:merlin:devicetype_import"

    def __init__(self, model=model, form=form, return_url=return_url, bulk_import_url=bulk_import_url):
        """Initialize DeviceTypeImport Bulk Import View."""
        BulkImportView.__init__(self, model, form, return_url, bulk_import_url)
