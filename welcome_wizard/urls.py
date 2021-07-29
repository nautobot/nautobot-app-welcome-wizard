"""Django urlpatterns declaration for Welcome Wizard plugin."""
from django.urls import path

from . import views

app_name = "welcome_wizard"

urlpatterns = [
    path("dashboard/", views.WelcomeWizardDashboard.as_view(), name="dashboard"),
    path("manufacturers/", views.ManufacturerListView.as_view(), name="manufacturer"),
    path("devicetypes/", views.DeviceTypeListView.as_view(), name="devicetype"),
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
]
