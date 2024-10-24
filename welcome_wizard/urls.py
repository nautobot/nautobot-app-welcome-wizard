"""Django urlpatterns declaration for Welcome Wizard app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "welcome_wizard"

urlpatterns = [
    path("dashboard/", views.WelcomeWizardDashboard.as_view(), name="dashboard"),
    path("manufacturers/", views.ManufacturerListView.as_view(), name="manufacturers"),
    path("manufacturer/<pk>", views.ManufacturerImportDetailView.as_view(), name="manufacturer"),
    path("devicetypes/", views.DeviceTypeListView.as_view(), name="devicetypes"),
    path("devicetype/<pk>", views.DeviceTypeImportDetailView.as_view(), name="devicetype"),
    path(
        "manufacturers/import/",
        views.ManufacturerBulkImportView.as_view(),
        name="manufacturer_import",
    ),
    path(
        "devicetypes/import/",
        views.DeviceTypeBulkImportView.as_view(),
        name="devicetype_import",
    ),
    path(
        "docs/",
        RedirectView.as_view(url=static("welcome_wizard/docs/index.html")),
        name="docs",
    ),
]
