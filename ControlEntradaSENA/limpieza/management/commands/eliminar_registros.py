from django.core.management.base import BaseCommand
from django.utils import timezone
from administrator.models import Ingresos, Salidas  # Ajusta según tu app
from administrator.models import Usuarios  # Ajusta según tu app
import os

class Command(BaseCommand):
    help = 'Elimina registros de ingresos y salidas según el rol del usuario y la fecha, registrando en log'

    def handle(self, *args, **kwargs):
        ROLES = {
            1: 'Instructor',
            2: 'Aprendiz',
            3: 'Visitante',
            4: 'Administrativo',
        }


        hoy = timezone.now().date()
        dia_semana = hoy.weekday()  # lunes=0 ... sábado=5

        if dia_semana == 5:
            roles_objetivo = [2, 3]  # Aprendiz y Visitante
        elif hoy.day == 1:
            roles_objetivo = [1, 4]  # Instructor y Administrativo
        else:
            self.stdout.write("Hoy no corresponde eliminar registros.")
            return

        ingresos_a_borrar = Ingresos.objects.filter(usuario__rol__in=roles_objetivo)
        salidas_a_borrar = Salidas.objects.filter(ingreso__in=ingresos_a_borrar)

        eliminados_ingresos = ingresos_a_borrar.count()
        eliminados_salidas = salidas_a_borrar.count()

        log_path = os.path.join("logs", "limpieza_detalle.log")
        with open(log_path, "a") as log_file:
            now = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            nombres_roles = [ROLES.get(r, f"Desconocido({r})") for r in roles_objetivo]
            log_file.write(f"\n[{now}] Iniciando limpieza automática para roles: {', '.join(nombres_roles)}\n")

            for salida in salidas_a_borrar:
                rol_nombre = salida.ingreso.usuario.rol.nombre
                log_file.write(f"[{now}] Eliminando SALIDA ID {salida.idsalida} | Usuario ID {salida.ingreso.usuario.documento} | Rol: {rol_nombre}\n")
            for ingreso in ingresos_a_borrar[:5]:  # Muestra los primeros 5 para ejemplo
                self.stdout.write(f"Ingreso ID {ingreso.idingreso} - Usuario ID {ingreso.usuario.documento} - Rol: {ingreso.usuario.rol.nombre}")

            salidas_a_borrar.delete()

            for ingreso in ingresos_a_borrar:
                rol_nombre = ingreso.usuario.rol.nombre
                log_file.write(f"[{now}] Eliminando INGRESO ID {ingreso.idingreso} | Usuario ID {ingreso.usuario.documento} | Rol: {rol_nombre}\n")
            
            ingresos_a_borrar.delete()

            log_file.write(f"[{now}] Limpieza finalizada: {eliminados_ingresos} ingresos y {eliminados_salidas} salidas eliminados.\n")

        self.stdout.write(self.style.SUCCESS(
            f"Eliminados {eliminados_ingresos} ingresos y {eliminados_salidas} salidas. Ver detalles en logs/limpieza_detalle.log"
        ))