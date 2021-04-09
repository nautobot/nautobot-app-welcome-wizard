# from nautobot.core.views import generic
from django.shortcuts import render
from django.views.generic import View

from merlin.models.importer import ManufacturerImport, DeviceTypeImport


class Home(View):
    """Display a randomly-selected Animal."""

    def get(self, request):
        manufacturer = ManufacturerImport.objects.order_by('?').first()
        device_types = DeviceTypeImport.objects.filter(manufacturer=manufacturer.pk)
        return render(request, 'merlin/home.html', {
            'manufacturer': manufacturer,
            'device_types': device_types
        })
