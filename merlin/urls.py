"""Django urlpatterns declaration for merlin plugin."""
from django.urls import path

from . import views

app_name = "merlin"

urlpatterns = [
    path("merlindashboard/", views.MerlinDashboard.as_view(), name="merlindashboard"),
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
