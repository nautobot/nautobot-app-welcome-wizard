"""API Urls for Merlin."""
from rest_framework import routers

from .views import ManufacturerViewSet, DeviceTypeViewSet


router = routers.DefaultRouter()
router.register("devicetypeimport", DeviceTypeViewSet)
router.register("manufacturerimport", ManufacturerViewSet)

app_name = "merlin-api"
urlpatterns = router.urls
