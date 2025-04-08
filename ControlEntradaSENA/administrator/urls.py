from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path("admin/", views.login_admin, name="login"),
    path("admin/logout", views.logout_admin, name="logout"),
    path("admin/registeradmin/", views.register_admin, name="registeradmin"),
    path("admin/inicio", views.adminpanel, name="adminpanel"),
    path("admin/users", views.users, name="users"),
    path("admin/users/registeruser/<int:rol>", views.register_user, name="registeruser"),
    path("admin/users/edituser/<int:id>", views.edit_user, name="edituser"),
    path("admin/sanciones", views.sanciones, name="penaltys"),
    path("admin/sanciones/editsanciones/<int:id>", views.edit_sanciones, name="editsanciones"),
    path("admin/dispositivo", views.dispositivo, name="devices"),
    path("admin/dispositivo/editdispositivo/<int:id>", views.edit_dispositivo, name="editdispositivo"),
    path("admin/vehiculos", views.vehicles, name="vehiculos"),
    path("admin/vehiculos/editvehiculo/<int:id>", views.edit_vehiculo, name="editvehiculo"),
    path("admin/about", views.about, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)