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
    path("admin/sanciones", views.fichas, name="penaltys"), 
    path("admin/crear_fichas", views.crear_fichas, name="crearfichas"), 
    path('cargar_users/<int:ficha_id>/', views.cargar_users, name='cargar_users'),
    path("admin/fichas", views.fichas, name="fichas"), 
    path("admin/sanciones/editsanciones/<int:id>", views.edit_sanciones, name="editsanciones"),
    path("admin/fichas/editfichas/<int:id>", views.edit_ficha, name="editficha"),
    path("admin/dispositivo", views.dispositivo, name="devices"),
    path("admin/create_dispositivo", views.create_dispositivo, name="create_device"),
    path("admin/dispositivo/editdispositivo/<int:id>", views.edit_dispositivo, name="editdispositivo"),
    path("admin/dispositivo/delete/<int:id>", views.delete_dispotivos, name="delete_dispositivo"), 
    path("admin/vehiculos", views.vehicles, name="vehiculos"),
    path("admin/create_vehiculo/", views.create_vehicle, name="create_vehiculo"),
    path("admin/vehiculos/editvehiculo/<int:id>", views.edit_vehiculo, name="editvehiculo"),
    path("admin/vehiculos/delete_vehiculo/<int:id>", views.delete_vehiculo, name="delete_vehiculo"),
    path("admin/reportes", views.reportes, name="reportes"),
    path("admin/reportes/excel", views.reporteInstructor, name="reporteInstructor"),
    path("admin/reportes/excelAprendiz", views.reporteAprendiz, name="reporteAprendiz"),
    path("admin/reportes/estadistico", views.informe_estadistico, name="informe_estadistico"),
    
    path("admin/about", views.about, name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)