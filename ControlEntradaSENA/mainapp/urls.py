from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:code>/access/", views.access, name="access"),
    path("<str:code>/registeruser/", views.registeruser, name="registeruser"),
    path("<str:code>/registervehicle/", views.registervehicle, name="registervehicle"),
    path("<str:code>/registerdevice/", views.registerdevice, name="registerdevice"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
