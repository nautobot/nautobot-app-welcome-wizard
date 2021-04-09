from rest_framework import routers

from .views import ManufacturerViewSet, DeviceTypeViewSet


router = routers.DefaultRouter()
router.register('device_type', DeviceTypeViewSet)
router.register('manufacturers', ManufacturerViewSet)
urlpatterns = router.urls