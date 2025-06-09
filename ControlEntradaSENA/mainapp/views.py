from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from administrator.models import Usuarios, Dispositivos, Vehiculos, Ingresos, Salidas, Extras,EstadoDispositivo
from administrator.forms import RegisterUser, RegisterDevice, RegisterVehicle, ExtrasForm
from datetime import datetime #Fecha y hora
#Inicio
from django.db.models import Q, Subquery
from django.utils.timezone import now

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

    if 'code' in request.GET:
        code = request.GET.get('code')
        form = ExtrasForm(request.POST or None, request.FILES or None)

        try:
            user = get_object_or_404(Usuarios, documento=code)

            vehiculos = Vehiculos.objects.filter(usuario=user.idusuario)
            rol = user.rol
            DocType = user.tipodocumento
            centro = user.centro or None
            ficha = user.ficha or None
            FichaName = ficha.nombre if ficha else None
            jornada = ficha.jornada if ficha else None

            dispositivos, status, ingreso_activo = determinar_modo(user)

            extras_ingreso = ingreso_activo.extras.all() if ingreso_activo else []
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
                'status': status,
            })

        except Http404:
            return redirect('registeruser', code=code)

    return render(request, 'index.html', {
        'title': 'Inicio',
        'ingresos': ingresos,
        'salidas': salidas
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
    date = datetime.now().strftime("%Y-%m-%d")
    hour = datetime.now().strftime("%H:%M:%S")

    ingreso = Ingresos.objects.filter(usuario=users.idusuario).exclude(idingreso__in=Salidas.objects.values('ingreso')).first()
    extras_ingreso = ingreso.extras.all() if ingreso else []

    if request.method == 'POST':
        idvehiculo = request.POST.get('vehicle')
        vehiculo = Vehiculos.objects.get(idvehiculo=idvehiculo) if idvehiculo else None

        dispositivos = request.POST.get('devices', '')
        dispositivos = dispositivos.split(',')

        dispositivo = Dispositivos.objects.get(iddispositivo=dispositivos[0]) if len(dispositivos) > 0 and dispositivos[0] else None
        dispositivo2 = Dispositivos.objects.get(iddispositivo=dispositivos[1]) if len(dispositivos) > 1 and dispositivos[1] else None
        dispositivo3 = Dispositivos.objects.get(iddispositivo=dispositivos[2]) if len(dispositivos) > 2 and dispositivos[2] else None

        descripcion = request.POST.get('descripcion')
        foto = request.FILES.get('foto')

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
                try:
                    extra_obj = Extras.objects.get(id=extra_id, ingreso=ingreso)
                    extra_obj.salida = salida
                    extra_obj.ingreso = None
                    extra_obj.save()
                except Extras.DoesNotExist:
                    continue

            if descripcion or foto:
                Extras.objects.create(
                    descripcion=descripcion,
                    foto=foto,
                    salida=salida
                )

            extras_salida = salida.extras.all()

            return render(request, 'access.html', {
                'title': f'{status} usuario',
                'users': users,
                'ingreso': ingreso,
                'salida': salida,
                'status': status,
                'extras_salida': extras_salida,
                'extras_ingreso': [],
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

            if descripcion or foto:
                Extras.objects.create(
                    descripcion=descripcion,
                    foto=foto,
                    ingreso=ingreso
                )

            extras_ingreso = ingreso.extras.all()

            return render(request, 'access.html', {
                'title': f'{status} usuario',
                'users': users,
                'ingreso': ingreso,
                'status': status,
                'extras_ingreso': extras_ingreso,
            })

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
    #Usuario predeterminado
    initial_data = {'usuario': users.idusuario}

    form = RegisterDevice(request.POST or None, request.FILES or None, initial=initial_data)
    form.fields['documento'].required = bool(doc)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.info(request, "success-device")
        return redirect(f'/?code={code}')

    return render(request, 'register/registerdevice.html',{
        'title': 'Registrar Dispositivo',
        'form': form,
        'doc': doc
    })





