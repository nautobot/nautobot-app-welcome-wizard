import importlib
from django.contrib import messages

from nautobot.circuits.api.serializers import *
from nautobot.core.api.serializers import *
from nautobot.dcim.api.serializers import *
from nautobot.ipam.api.serializers import *
from nautobot.tenancy.api.serializers import *
from nautobot.virtualization.api.serializers import *

class Prerequisites(object):
    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        response = self.get_request(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path_info.endswith("/add/"):
            # model = view_func.view_class.model_form.Meta.model
            try:
                # It wouldn't be a hackathon without some hacks
                serializer = eval(f"{view_func.view_class.model_form.Meta.model.__name__}Serializer")
                serial = serializer()
                for field in serial.fields.values():
                    if field.required:
                        if getattr(field, "Meta", False) and not field.Meta.model.objects.all():
                            messages.error(request, f"You need to configure a {field.label} before you create this item.")
            except Exception as e:
                print(e)
