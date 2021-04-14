import logging

from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from merlin.jobs import MerlinImportDeviceType, MerlinImportManufacturer
from merlin.tables import ManufacturerTable, DeviceTypeTable
from merlin.filters import DeviceTypeImportFilterSet, ManufacturerImportFilterSet
from merlin.forms import DeviceTypeImportFilterForm, DeviceTypeBulkImportForm, ManufacturerImportFilterForm, ManufacturerBulkImportForm
from nautobot.extras.models import JobResult
from nautobot.core.views import generic

from merlin.models.importer import ManufacturerImport, DeviceTypeImport

logger = logging.getLogger(__name__)

class ManufacturerListView(generic.ObjectListView):
    """Table of all Manufacturers discovered in the Git Repository."""
    table = ManufacturerTable
    queryset = ManufacturerImport.objects.all()
    action_buttons = None
    template_name = "merlin/manufacturer.html"
    filterset = ManufacturerImportFilterSet
    filterset_form = ManufacturerImportFilterForm


#class ManufacturerImportView(View):


class DeviceTypeListView(generic.ObjectListView):
    """Table of Device Types based on the Manufacturer."""
    table=DeviceTypeTable
    queryset = DeviceTypeImport.objects.prefetch_related("manufacturer")
    filterset = DeviceTypeImportFilterSet
    action_buttons = None
    template_name = "merlin/devicetype.html"
    filterset_form = DeviceTypeImportFilterForm


class BulkImportView(View):

    def __init__(self, model, form, return_url, bulk_import_url):
        self.model = model
        self.form = form
        self.return_url = return_url
        self.bulk_import_url = bulk_import_url

    def get(self, request):
        if not request.GET.get('pk'):
            return redirect("plugins:merlin:manufacturer")
        pk = request.GET['pk']
        initial = {'pk': [pk]}

        obj = self.model.objects.get(pk=pk)
        form = self.form(initial)

        return render(
            request,
            'merlin/import.html',
            {
                "form": form,
                'obj': obj,
                'return_url': self.return_url,
                'bulk_import_url': self.bulk_import_url
            },
        )

    
    def post(self, request):
        if request.method != 'POST':
            return redirect(self.return_url)
        form = self.form(request.POST)
        if form.is_valid():
            logger.debug("Form validation was successful")
            pk_list = request.POST.getlist("pk")
            onboarded = []

            for obj in self.model.objects.filter(pk__in=pk_list):
                if self.model == ManufacturerImport:
                    data = {
                        'manufacturer': obj.name
                    }
                    job = MerlinImportManufacturer()
                    job.job_result = JobResult()
                    job.run(data, commit=True)
                    onboarded.append(obj.name)
                
                elif self.model == DeviceTypeImport:
                    job = MerlinImportDeviceType()
                    data = {
                        "device_type": obj.filename
                    }
                    job.job_result = JobResult()
                    job.run(data, commit=True)
                    onboarded.append(obj.name)
            
            messages.success(request, "Onboarded {} objects.".format(len(onboarded)))

        return redirect(self.return_url)


class ManufacturerBulkImportView(BulkImportView):
    model = ManufacturerImport
    form = ManufacturerBulkImportForm
    return_url = "plugins:merlin:manufacturer"
    bulk_import_url = "plugins:merlin:manufacturer_import"

    def __init__(self, model=model, form=form, return_url=return_url, bulk_import_url=bulk_import_url):
        BulkImportView.__init__(self, model, form, return_url, bulk_import_url)


class DeviceTypeBulkImportView(BulkImportView):
    model = DeviceTypeImport
    form = DeviceTypeBulkImportForm
    return_url = "plugins:merlin:devicetype"
    bulk_import_url = "plugins:merlin:devicetype_import"

    def __init__(self, model=model, form=form, return_url=return_url, bulk_import_url=bulk_import_url):
        BulkImportView.__init__(self, model, form, return_url, bulk_import_url)