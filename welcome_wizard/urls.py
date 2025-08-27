# urls.py
from nautobot.apps.urls import NautobotUIViewSetRouter
from . import views
from .views import ManufacturerListView, DeviceTypeListView, WelcomeWizardDashboard
from django.urls import path

app_name = "welcome_wizard"

router = NautobotUIViewSetRouter()
router.register("manufacturers", views.ManufacturerListView, basename="manufacturerimport")
router.register("devicetypes", views.DeviceTypeListView, basename="devicetypeimport")
router.register("dashboard", views.WelcomeWizardDashboard, basename="dashboard")

# ALIAS to keep the old URL working
manufacturer_import_view = ManufacturerListView.as_view({"get": "bulk_import", "post": "bulk_import"})
devicetype_import_view   = DeviceTypeListView.as_view({"get": "bulk_import", "post": "bulk_import"})

manufacturers_list_view = ManufacturerListView.as_view({"get": "list"})
devicetypes_list_view   = DeviceTypeListView.as_view({"get": "list"})
dashboard_list_view = WelcomeWizardDashboard.as_view({"get": "list"})

urlpatterns = [
    path("manufacturers/", manufacturers_list_view, name="manufacturers"),
    path("devicetypes/",   devicetypes_list_view,  name="devicetypes"),
    path("dashboard/", dashboard_list_view, name="dashboard"),
    path("manufacturers/import/", manufacturer_import_view, name="manufacturer_import"),
    path("devicetypes/import/",   devicetype_import_view,   name="devicetype_import"),
] + router.urls