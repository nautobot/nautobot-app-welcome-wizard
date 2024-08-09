"""Middleware for the Welcome Wizard app."""

import logging

from django.contrib import messages
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from nautobot.core.templatetags.helpers import bettertitle

logger = logging.getLogger("welcome_wizard.middleware")


class Prerequisites:
    """Middleware for determining prerequisites and adding notifications."""

    def __init__(self, get_request):
        """Capture the request on the initialization."""
        self.get_request = get_request

    def __call__(self, request):
        """Capture the response and return it."""
        return self.get_request(request)

    def process_view(self, request, view_func, view_args, view_kwargs):  # pylint: disable=unused-argument
        """Process the view to determine if it's one we want to intercept."""
        # If no user or they aren't authenticated, return to hit the default login redirect
        if not hasattr(request, "user") or not request.user.is_authenticated:
            return
        if request.path.endswith("/add/"):
            # Check if using a Nautobot view class.
            if (
                hasattr(view_func, "view_class")
                and hasattr(view_func.view_class, "model_form")
                and view_func.view_class.model_form is not None
            ):
                base_fields = view_func.view_class.model_form.base_fields
            # Check if using a NautobotUIViewSet class.
            elif (
                hasattr(view_func, "cls")
                and hasattr(view_func.cls, "form_class")
                and view_func.cls.form_class is not None
            ):
                base_fields = view_func.cls.form_class.base_fields
            else:
                return

            for field in base_fields:
                if (
                    base_fields[field].required
                    and hasattr(base_fields[field], "queryset")
                    and not base_fields[field].queryset.exists()
                ):
                    meta = base_fields[field].queryset.model._meta
                    try:
                        reverse_link = reverse(f"{meta.app_label}:{meta.model_name}_add")
                    except NoReverseMatch as error:
                        logger.warning("No Reverse Match was found for %s. %s", bettertitle(meta.verbose_name), error)
                        reverse_link = ""
                    msg = format_html(
                        "You need to configure a <a href='{}'>{}</a> before you create this item.",
                        reverse_link,
                        bettertitle(meta.verbose_name),
                    )
                    messages.error(request, msg)
