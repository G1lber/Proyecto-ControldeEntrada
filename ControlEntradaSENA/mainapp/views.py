from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from administrator.models import Usuarios, Dispositivos, Vehiculos, Ingresos, Salidas, Extras,EstadoDispositivo
from administrator.forms import RegisterUser, RegisterDevice, RegisterVehicle, ExtrasForm
from datetime import datetime #Fecha y hora
#Inicio
from django.db.models import Q, Subquery
from django.utils.timezone import now
from django.db import transaction
from django.core.files.storage import default_storage


def determinar_modo(user):
    dispositivos_usuario = Dispositivos.objects.filter(usuario=user.idusuario)

    ingreso_activo = Ingresos.objects.filter(usuario=user.idusuario).exclude(
        idingreso__in=Salidas.objects.values('ingreso')
    ).first()

    if ingreso_activo:
        # SALIDA
        ids_dentro = EstadoDispositivo.objects.filter(
            estado='dentro',
            dispositivo__usuario=user.idusuario
        ).values_list('dispositivo_id', flat=True)

        dispositivos = dispositivos_usuario.filter(iddispositivo__in=ids_dentro)
        status = 'Salida'
    else:
        # INGRESO
        ids_fuera = EstadoDispositivo.objects.filter(
            estado='fuera',
            dispositivo__usuario=user.idusuario
        ).values_list('dispositivo_id', flat=True)

        dispositivos_sin_estado = dispositivos_usuario.exclude(
            iddispositivo__in=EstadoDispositivo.objects.values_list('dispositivo_id', flat=True)
        )

        dispositivos = dispositivos_usuario.filter(iddispositivo__in=ids_fuera) | dispositivos_sin_estado
        status = 'Ingreso'

    return dispositivos.distinct(), status, ingreso_activo

def index(request):
    ingresos = Ingresos.objects.exclude(idingreso__in=Subquery(Salidas.objects.values('ingreso')))
    salidas = Salidas.objects.all()

    status = request.GET.get("status")  # Captura si viene de ingreso/salida

    if 'code' in request.GET:
        code = request.GET.get('code')
        form = ExtrasForm(request.POST or None, request.FILES or None)
        if code =="" or code is None: 
            return redirect('index')
        try:
            user = get_object_or_404(Usuarios, documento=code)

            vehiculos = Vehiculos.objects.filter(usuario=user.idusuario)
            rol = user.rol
            DocType = user.tipodocumento
            centro = user.centro or None
            ficha = user.ficha or None
            FichaName = ficha.nombre if ficha else None
            jornada = ficha.jornada if ficha else None

            dispositivos, modo_status, ingreso_activo = determinar_modo(user)

            extras_ingreso = Extras.objects.filter(
                salida__isnull=True,
                ingreso__usuario=user
            )
            dispositivo_salida = Dispositivos.objects.filter(usuario=user.idusuario, documento__isnull=False).first()

            return render(request, 'index.html', {
                'title': user,
                'users': user,
                'DocType': DocType,
                'centro': centro,
                'rol': rol,
                'ficha': ficha,
                'FichaName': FichaName,
                'jornada': jornada,
                'vehiculos': vehiculos,
                'dispositivos': dispositivos,
                'extra': form,
                'extras_ingreso': extras_ingreso,
                'salida': ingreso_activo,
                'dispositivo_salida': dispositivo_salida,
                'status': modo_status,  # status real del usuario
            })

        except Http404:
            return redirect('registeruser', code=code)

    return render(request, 'index.html', {
        'title': 'Inicio',
        'ingresos': ingresos,
        'salidas': salidas,
        'status': status  # status de ingreso/salida para el JS si aplica
    })


def idispositivos(request):
    # sourcery skip: extract-method, use-fstring-for-concatenation

    #Traer los ingresos que no estan relacionados con una salida
    ingresos = Ingresos.objects.exclude(idingreso__in=Subquery(Salidas.objects.values('ingreso'))) or None 
    #Traer salidas
    salidas = Salidas.objects.all()
    #Recibir codigo por GET
    if 'code' in request.GET:
        code = request.GET.get('code')

        #Si el dispositivo esta registrado
        try:
            #Buscar dispositivo por su SN
            dispostivo = get_object_or_404(Dispositivos, sn=code) 
            print(dispostivo)
            if dispostivo.usuario:
                user = get_object_or_404(Usuarios, idusuario=dispostivo.usuario.idusuario)
            #Traer todos los datos del usuario
            vehiculos = Vehiculos.objects.filter(usuario=user.idusuario)
            dispositivos = Dispositivos.objects.filter(usuario=user.idusuario)
            rol = user.rol
            DocType = user.tipodocumento 
            centro = user.centro or None
            ficha = user.ficha or None
            FichaName = ficha.nombre if ficha else None
            jornada = ficha.jornada if ficha else None
            
            #Si el usuario toma su foto: Guardarla
            if request.method == 'POST':   
                user.imagen.delete()
                imagen = request.FILES['imagen']
                extension = imagen.name.split('.')[-1].lower()
                filename = f"{code}.{extension}"
                imagen.name = filename                        
                user.imagen = imagen
                user.save()
                return redirect(f"/?code={code}")
                                
            #Si el usuario tiene un ingreso activo, hacer salida
            salida = Ingresos.objects.filter(usuario=user.idusuario).exclude(idingreso__in=Salidas.objects.values('ingreso')).first() or None
            dispositivo_salida = Dispositivos.objects.filter(usuario=user.idusuario, documento__isnull=False).first()

            print(salida)

            return render(request, 'dipositivos.html',{
                #Para ingreso
                'title': user,          
                'users': user,                
                'DocType': DocType,
                'centro': centro,
                'rol': rol,
                'ficha': ficha,
                'FichaName': FichaName,
                'jornada': jornada,
                'vehiculos': vehiculos,
                'dispositivos': dispositivos,
                #Para salida
                'salida': salida,
                'dispositivo_salida': dispositivo_salida,
                })
        #Si el dispositvo no existe
        except Http404:
            return redirect('index')
    
    return render(request, 'dipositivos.html', {
        'title': 'Inicio',
        'ingresos': ingresos,
        'salidas': salidas
    })
#Ingreso y salida

def access(request, code):
    users = get_object_or_404(Usuarios, documento=code)
    date = now().date()
    hour = now().time()

    ingreso = Ingresos.objects.filter(usuario=users.idusuario).exclude(
        idingreso__in=Salidas.objects.values('ingreso')
    ).first()
    extras_ingreso = ingreso.extras.all() if ingreso else []

    if request.method == 'POST':
        idvehiculo = request.POST.get('vehicle')
        vehiculo = Vehiculos.objects.filter(idvehiculo=idvehiculo).first() if idvehiculo else None

        dispositivos_raw = request.POST.get('devices', '')
        dispositivos_ids = [int(i) for i in dispositivos_raw.split(',') if i.isdigit()]
        dispositivos = Dispositivos.objects.filter(iddispositivo__in=dispositivos_ids)

        dispositivo = dispositivos[0] if len(dispositivos) > 0 else None
        dispositivo2 = dispositivos[1] if len(dispositivos) > 1 else None
        dispositivo3 = dispositivos[2] if len(dispositivos) > 2 else None

        descripcion = request.POST.get('descripcion')
        foto = request.FILES.get('foto')
        foto_tipo = request.POST.get('foto_tipo', 'extra')

        try:
            with transaction.atomic():
                if ingreso:
                    # SALIDA
                    salida = Salidas.objects.create(
                        fecha=date,
                        ingreso=ingreso,
                        vehiculo=vehiculo,
                        dispositivo=dispositivo,
                        dispositivo2=dispositivo2,
                        dispositivo3=dispositivo3,
                        horasalida=hour
                    )
                    status = "Salida"

                    for d in [dispositivo, dispositivo2, dispositivo3]:
                        if d:
                            EstadoDispositivo.objects.update_or_create(
                                dispositivo=d,
                                defaults={'estado': 'fuera'}
                            )

                    extras_ids = request.POST.getlist('extras_to_move')
                    for extra_id in extras_ids:
                        extra_obj = Extras.objects.filter(id=extra_id, ingreso=ingreso, salida__isnull=True).first()
                        if extra_obj:
                            extra_obj.ingreso = None
                            extra_obj.salida = salida
                            extra_obj.save()

                    if foto and foto_tipo == 'usuario':
                        if users.imagen:
                            users.imagen.delete()
                        extension = foto.name.split('.')[-1].lower()
                        filename = f"{users.documento}.{extension}"
                        foto.name = filename
                        users.imagen.save(filename, foto, save=True)
                    elif descripcion or foto:
                        Extras.objects.create(
                            descripcion=descripcion,
                            foto=foto,
                            salida=salida
                        )

                    return render(request, 'access.html', {
                        'title': f'{status} usuario',
                        'users': users,
                        'status': status,
                    })

                else:
                    # INGRESO
                    ingreso = Ingresos.objects.create(
                        fecha=date,
                        usuario=users,
                        vehiculo=vehiculo,
                        dispositivo=dispositivo,
                        dispositivo2=dispositivo2,
                        dispositivo3=dispositivo3,
                        horaingreso=hour
                    )
                    status = "Ingreso"

                    for d in [dispositivo, dispositivo2, dispositivo3]:
                        if d:
                            EstadoDispositivo.objects.update_or_create(
                                dispositivo=d,
                                defaults={'estado': 'dentro'}
                            )

                    extras_pendientes = Extras.objects.filter(
                        salida__isnull=True,
                        ingreso__usuario=users
                    ).exclude(ingreso=ingreso)
                    for extra in extras_pendientes:
                        extra.ingreso = ingreso
                        extra.save()

                    # FOTO USUARIO
                    if foto and foto_tipo == 'usuario':
                        if users.imagen:
                            users.imagen.delete()
                        extension = foto.name.split('.')[-1].lower()
                        filename = f"{users.documento}.{extension}"
                        foto.name = filename
                        users.imagen.save(filename, foto, save=True)

                    # FOTO EXTRA
                    elif (foto and foto_tipo == 'extra') or descripcion:
                        if foto and foto_tipo == 'extra':
                            extension = foto.name.split('.')[-1].lower()

                            # Contar cuántos extras ya tiene este usuario
                            cantidad_extras = Extras.objects.filter(ingreso__usuario=users).count()
                            numero_extra = cantidad_extras + 1

                            # Construir nombre de archivo único
                            filename = f"extras/extra_{users.documento}_{numero_extra}.{extension}"

                            # Eliminar si por alguna razón ya existe
                            if default_storage.exists(filename):
                                default_storage.delete(filename)

                            foto.name = filename
                        Extras.objects.create(
                            descripcion=descripcion,
                            foto=foto,
                            ingreso=ingreso
                        )

                    return render(request, 'access.html', {
                        'title': f'{status} usuario',
                        'users': users,
                        'status': status,
                    })

        except Exception as e:
            print("Error en transacción:", e)

    return render(request, 'access.html', {
        'title': 'Acceso usuario',
        'users': users,
        'status': None,
        'ingreso': ingreso,
        'extras_ingreso': extras_ingreso,
    })
#Registrar usuario
def registeruser(request, code):
    rol = request.GET.get('rol') #Obtener rol a registrar por GET
    initial_data = {'rol': rol, 'rol_hide': rol , 'documento': code} #Dato predeterminado del rol y documento
    form = RegisterUser(request.POST or None, request.FILES or None, initial=initial_data)

    #Requerir o no campos de formulario segun el rol
    form.fields['centro'].required = rol != "3"
    form.fields['ficha'].required = rol == "2"

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, "success-user")
        return redirect('index')

    return render(request, 'register/registeruser.html', {
        'title': 'Registrar usuario',
        'rol': rol,
        'form': form
    })


#Registrar vehiculo
def registervehicle(request, code):
    users = Usuarios.objects.get(documento=code)
    rol = users.rol.nombre.lower()
    
    #Tipo vehiculo
    vehicle = request.GET.get('vehicle')

    #Tipo vehiculo y usuario predeterminados
    initial_data = {'tipo': vehicle, 'usuario': users.idusuario}

    form = RegisterVehicle(request.POST or None, request.FILES or None, initial=initial_data, rol=rol, user=users)


    form.fields['placa'].required = vehicle != "3"
    form.fields['modelo'].required = vehicle != "3"

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, "success-vehicle")
        return redirect(f'/?code={code}')
    return render(request, 'register/registervehicle.html',{
        
        'title': 'Registrar Vehiculo',
        'vehicle': vehicle,
        'form': form,
        'users': users
    })

#Registrar dispositivo
def registerdevice(request, code):
    doc = request.GET.get('doc')

    users = Usuarios.objects.get(documento=code)
    initial_data = {'usuario': users.idusuario}

    form = RegisterDevice(request.POST or None, request.FILES or None, initial=initial_data)
    form.fields['documento'].required = bool(doc)

    if request.method == 'POST' and form.is_valid():
        dispositivo = form.save()

        # Detectar si el usuario tiene un ingreso activo
        tiene_ingreso_pendiente = Ingresos.objects.filter(
            usuario=users.idusuario
        ).exclude(idingreso__in=Salidas.objects.values('ingreso')).exists()

        estado = 'dentro' if tiene_ingreso_pendiente else 'fuera'

        EstadoDispositivo.objects.update_or_create(
            dispositivo=dispositivo,
            defaults={'estado': estado}
        )

        messages.info(request, "success-device")
        return redirect(f'/?code={code}&nuevo_dispositivo=true')

    return render(request, 'register/registerdevice.html', {
        'title': 'Registrar Dispositivo',
        'form': form,
        'doc': doc,
        'users': users
    })


