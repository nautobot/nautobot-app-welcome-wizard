# urls.py
from nautobot.apps.urls import NautobotUIViewSetRouter
from . import views

app_name = "welcome_wizard"

router = NautobotUIViewSetRouter()
router.register("manufacturers", views.ManufacturerListView, basename="manufacturerimport")
router.register("devicetypes", views.DeviceTypeListView, basename="devicetypeimport")
router.register("dashboard", views.WelcomeWizardDashboard, basename="dashboard")

urlpatterns = router.urls
