"""Django API urlpatterns declaration for welcome_wizard app."""

from nautobot.apps.api import OrderedDefaultRouter

from welcome_wizard.api import views

router = OrderedDefaultRouter()
# add the name of your api endpoint, usually hyphenated model name in plural, e.g. "my-model-classes"
router.register("manufacturer-imports", views.ManufacturerImportViewSet)

app_name = "welcome_wizard-api"
urlpatterns = router.urls
