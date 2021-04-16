import importlib
from django.contrib import messages


class Prerequisites(object):
    def __init__(self, get_request):
        self.get_request = get_request

    def __call__(self, request):
        response = self.get_request(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # If no user or they aren't authenticated, return to hit the default login redirect
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return
        if request.path_info.endswith("/add/"):
            # model = view_func.view_class.model_form.Meta.model
            try:
                base_fields = view_func.view_class.model_form.base_fields
                for field in base_fields:
                    if base_fields[field].required:
                        if hasattr(base_fields[field], "queryset") and not base_fields[field].queryset:
                            name = field.replace("_", " ").title()
                            messages.error(request, f"You need to configure a {name} before you create this item.")
            except Exception as e:
                print(e)
