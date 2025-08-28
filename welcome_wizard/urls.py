# urls.py
from nautobot.apps.urls import NautobotUIViewSetRouter
from . import views
from django.urls import path
from django.templatetags.static import static
from django.views.generic import RedirectView

app_name = "welcome_wizard"

router = NautobotUIViewSetRouter()
router.register("manufacturers", views.ManufacturerListView, basename="manufacturerimport")
router.register("devicetypes",  views.DeviceTypeListView,   basename="devicetypeimport")
router.register("dashboard",    views.WelcomeWizardDashboard, basename="dashboard")

urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("welcome_wizard/docs/index.html")), name="docs"),
] + router.urls
