"""Middleware for the Merlin plugin."""
from django.contrib import messages
from django.urls import reverse
from django.utils.safestring import mark_safe


class Prerequisites:
    """Middleware for determining prerequisites and adding notifications."""

    def __init__(self, get_request):
        """Capture the request on the initialization."""
        self.get_request = get_request

    def __call__(self, request):
        """Capture the response and return it."""
        response = self.get_request(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):  # pylint: disable=W0613,R0201
        """Process the view to determine if it's one we want to intercept."""
        # If no user or they aren't authenticated, return to hit the default login redirect
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return
        if request.path.endswith("/add/"):
            # model = view_func.view_class.model_form.Meta.model
            try:
                base_fields = view_func.view_class.model_form.base_fields
                for field in base_fields:
                    if base_fields[field].required:
                        if hasattr(base_fields[field], "queryset") and not base_fields[field].queryset:
                            name = (
                                base_fields[field].label
                                if base_fields[field].label
                                else field.replace("_", " ").title()
                            )
                            reverse_name = field.replace("_", "")
                            reverse_link = reverse(f"{request.resolver_match.app_names[0]}:{reverse_name}_add")
                            msg = f"You need to configure a <a href='{reverse_link}'>{name}</a> before you create this item."  # nosec
                            messages.error(request, mark_safe(msg))
            except Exception as error:  # pylint: disable=broad-except
                print(error)
