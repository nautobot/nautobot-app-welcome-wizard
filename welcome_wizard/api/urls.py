"""API Urls for Welcome Wizard."""
from rest_framework import routers

from .views import ManufacturerViewSet, DeviceTypeViewSet


router = routers.DefaultRouter()
router.register("devicetypeimport", DeviceTypeViewSet)
router.register("manufacturerimport", ManufacturerViewSet)

app_name = "welcome_wizard-api"
urlpatterns = router.urls
