# urls.py
from nautobot.apps.urls import NautobotUIViewSetRouter
from . import views
from .views import ManufacturerListView, DeviceTypeListView, WelcomeWizardDashboard
from django.urls import path
from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView

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

manufacturer_detail_view = ManufacturerListView.as_view({"get": "retrieve"})
devicetype_detail_view   = DeviceTypeListView.as_view({"get": "retrieve"})

urlpatterns = [
    path("manufacturers/", manufacturers_list_view, name="manufacturers"),
    path("devicetypes/",   devicetypes_list_view,  name="devicetypes"),
    path("dashboard/", dashboard_list_view, name="dashboard"),
    path("manufacturers/import/", manufacturer_import_view, name="manufacturer_import"),
    path("devicetypes/import/",   devicetype_import_view,   name="devicetype_import"),
    path("manufacturer/<pk>", manufacturer_detail_view, name="manufacturer"),
    path("devicetype/<pk>", devicetype_detail_view, name="devicetype"),
    path("docs/", RedirectView.as_view(url=static("welcome_wizard/docs/index.html")), name="docs"),
] + router.urls