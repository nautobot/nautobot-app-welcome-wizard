"""Django urlpatterns declaration for merlin plugin."""
from django.urls import path

from . import views

app_name = "merlin"

urlpatterns = [
    path("home/", views.Home.as_view(), name="home"),
]
