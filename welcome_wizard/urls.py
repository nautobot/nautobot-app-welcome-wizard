"""Django urlpatterns declaration for welcome_wizard app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter

from . import views

app_name = "welcome_wizard"

router = NautobotUIViewSetRouter()
router.register("manufacturers", views.ManufacturerImportUIViewSet, basename="manufacturerimport")
router.register("devicetypes", views.DeviceTypeImportUIViewSet, basename="devicetypeimport")
router.register("moduletypes", views.ModuleTypeImportUIViewSet, basename="moduletypeimport")
router.register("dashboard", views.MerlinUIViewSet, basename="dashboard")

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("welcome_wizard/docs/index.html")), name="docs"),
] + router.urls
