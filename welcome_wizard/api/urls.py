"""Django API urlpatterns declaration for welcome_wizard app."""

from nautobot.apps.api import OrderedDefaultRouter

from welcome_wizard.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("manufacturerimport", views.ManufacturerImportViewSet)
router.register("devicetypeimport", views.DeviceTypeImportViewSet)

urlpatterns = router.urls
