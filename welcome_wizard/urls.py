"""Django urlpatterns declaration for welcome_wizard app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter


from welcome_wizard import views


app_name = "welcome_wizard"
router = NautobotUIViewSetRouter()

# The standard is for the route to be the hyphenated version of the model class name plural.
# for example, ExampleModel would be example-models.
router.register("manufacturer-imports", views.ManufacturerImportUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("welcome_wizard/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
