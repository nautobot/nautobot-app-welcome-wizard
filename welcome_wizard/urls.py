"""Django urlpatterns declaration for welcome_wizard app."""

from django.templatetags.static import static
from django.urls import path
from django.views.generic import RedirectView
from nautobot.apps.urls import NautobotUIViewSetRouter


from welcome_wizard import views


router = NautobotUIViewSetRouter()

router.register("manufacturerimport", views.ManufacturerImportUIViewSet)


urlpatterns = [
    path("docs/", RedirectView.as_view(url=static("welcome_wizard/docs/index.html")), name="docs"),
]

urlpatterns += router.urls
