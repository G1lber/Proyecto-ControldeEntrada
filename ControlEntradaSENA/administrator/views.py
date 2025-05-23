from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.db import connection
from .forms import *
from django.db.models import Q

#Login admin
@user_passes_test(lambda u: not u.is_authenticated, login_url='adminpanel') #Si el usuario ya esta logeado no va a poder acceder a la pagina de login 
def login_admin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username, password=password)
        
        if admin is not None:
            login(request, admin)
            return redirect('adminpanel')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'login.html', {
        'title': 'Iniciar Sesion',
    })

#Logout admin
def logout_admin(request):
    logout(request)
    return redirect('login')

#Registro admin
def register_admin(request):
    form = RegisterForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('login')
        
    return render(request, 'register.html', {
        'title': 'Añadir administrador',
        'form': form
    })


#AdminPanel
@login_required(login_url="login")
def adminpanel(request):
    return render(request, 'adminpanel.html')

######

#Lista usuarios
@login_required(login_url="admin")
def users(request):
    users = Usuarios.objects.all().prefetch_related('dispositivos_set').prefetch_related('vehiculos_set')
    
    search_query = request.GET.get('search')
    #Buscar usuarios
    if search_query:
        users = users.filter(
            Q(nombres__icontains=search_query) | Q(documento__icontains=search_query)
        )  
    if not users.exists():  #Luego revisamos si el resultado está vacío
        messages.warning(request, "No se encontraron usuarios con esa búsqueda.")
        
    checks = request.POST.get('checks-users')
    if checks:
        checks = checks.split(',')
        Usuarios.objects.filter(idusuario__in=checks).delete()
        messages.success(request, "Se han eliminado los usuarios seleccionados")

    delete = request.POST.get('delete-user')
    if delete:
        Usuarios.objects.filter(idusuario=delete).delete()
        messages.success(request, "Se ha eliminado el usuario")
    
    return render(request, 'pages/usuarios/users.html', {
        'title': 'Usuarios',
        'users': users
    })

#Registrar usuario
def register_user(request, rol):
    initial = {'rol': rol}
    form = RegisterUser(request.POST or None, request.FILES or None, initial=initial)

    form.fields['centro'].required = False if rol == 3 else True
    form.fields['ficha'].required = False if rol != 2 else True

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('users')

    return render(request, 'pages/usuarios/register.html', {
        'title': 'Registrar usuario',
        'form': form,
        'rol': rol,
    })

#Editar usuario
def edit_user(request, id):
    instance = Usuarios.objects.get(idusuario=id)
    initial = {
        'imagen': instance.imagen,
        'rol': instance.rol,
        'rol_hide': instance.rol
    }
    
    form = RegisterUser(request.POST or None, request.FILES or None, instance=instance, initial=initial)

    form.fields['imagen'].required = False
    form.fields['centro'].required = False if instance.rol == 3 else True
    form.fields['ficha'].required = False if instance.rol != 2 else True
    form.fields['rol'].disabled = True  
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha editado correctamente")
            return redirect('users')

    return render(request, 'pages/usuarios/edit.html', {
        'title': 'Editar usuario',
        'form': form,
    })

###

# Lista de dispositivos
@login_required(login_url="admin")
def dispositivo(request):
    devices = Dispositivos.objects.all() 
    query = request.GET.get('search', '')
    if query:
        devices = Dispositivos.objects.filter(sn__icontains=query)
        if not devices.exists():  #Luego revisamos si el resultado está vacío
            messages.warning(request, "No se encontraron dispositivos con esa búsqueda.")

    return render(request, 'pages/dispositivos/devices.html', {
        'title': 'Dispositivos',
        'dispositivos': devices,
        'search': query,
    })

def create_dispositivo(request):
    form = RegisterDevice(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('devices')
    return render(request, "pages/dispositivos/crear.html",{
        "form":form
    })
#Editar dispositivo
def edit_dispositivo(request, id):
    instance = Dispositivos.objects.get(iddispositivo=id)
    form = RegisterDevice(request.POST or None, request.FILES or None, instance= instance)
    if request .method == "POST" :


        if form.is_valid():
            form.save()
            messages.success(request, "se ha editado correctamente")
            return redirect('devices')
    return render(request, 'pages/dispositivos/edit.html', {
        'title': 'Editar dispositivo',
        'form': form
    })
#Eliminar dispositivo Individual
def delete_dispotivos(request, id):
        device = get_object_or_404(Dispositivos, iddispositivo=id)
        device.delete()
        return redirect("devices")

###

#Sanciones
@login_required(login_url="admin")
def sanciones(request):
    sanciones = Sanciones.objects.all()
    
    return render(request, 'pages/sanciones/sanciones.html', {
        'title': 'Sanciones',
        'penaltys': sanciones
    })

# Crear Fichas
@login_required(login_url="admin")
def crear_fichas(request):
    if request.method == 'POST':
        post_data = request.POST.copy()  # hacemos copia para modificarlo
        nombre_id = post_data.get('nombre')

        # Si el nombre no es un ID numérico, lo escribió el usuario y hay que crearlo
        if nombre_id and not nombre_id.isdigit():
            nuevo_nombre = FichasNombre.objects.create(nombre=nombre_id)
            post_data['nombre'] = nuevo_nombre.idfichanombre  # reescribimos con el ID real

        form = RegisterFicha(post_data)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha creado correctamente")
            return redirect('fichas')
    else:
        form = RegisterFicha()

    return render(request, 'pages/fichas/crear.html', {
        'form': form
    })

#Fichas
@login_required(login_url="admin")
def fichas(request):
    search_query = request.GET.get('search', '')
    fichas = Fichas.objects.all()

    if search_query:
        fichas = fichas.filter(
            Q(nombre__nombre__icontains=search_query) |
            Q(jornada__nombre__icontains=search_query) |
            Q(numero__icontains=search_query) 
        )
        if not fichas.exists():
            messages.warning(request, "No se encontraron fichas con esa búsqueda.")

    return render(request, 'pages/fichas/fichas.html', {
        'title': 'Fichas',
        'fichas': fichas
    })


#Editar Fichas

def edit_ficha(request, id):
    instance = Fichas.objects.get(idficha=id)
    form = RegisterFicha(request.POST or None, instance=instance)

    if request.method == "POST":
        if form.is_valid():
            # Restauramos los campos deshabilitados manualmente
            form.instance.nombre = instance.nombre
            form.instance.tipo = instance.tipo
            form.save()
            messages.success(request, "Se ha editado correctamente")
            return redirect('fichas')

    return render(request, 'pages/fichas/edit.html', {
        'title': 'Editar Fichas',
        'form': form
    })

#Editar sanciones

def edit_sanciones(request, id):
    instance=Sanciones.objects.get(idsancion=id)

    form = RegisterSanciones(request.POST or None, request.FILES or None, instance= instance)
    if request .method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, "se ha editado correctamente")
            return redirect('sanciones')
            
    return render(request, 'pages/sanciones/edit.html', {
        'title': 'Editar Sanciones',
        'form': form
     })


#Vehicles
@login_required(login_url="admin")
def vehicles(request):
    search_query = request.GET.get('search', '')  # Obtiene el término de búsqueda desde la URL
    print(f"Search query: {search_query}")  # Para verificar que estamos recibiendo la búsqueda
    
    # Inicializar vehicles por defecto
    vehicles = Vehiculos.objects.all()  # Por defecto, mostrar todos los vehículos
    
    if search_query:  # Si hay un término de búsqueda
        vehicles = Vehiculos.objects.filter(placa__icontains=search_query)  # Filtra por placa
    if not vehicles:
        messages.warning(request, "No se encontraron vehiculos con esa búsqueda.")
    
    return render(request, 'pages/vehiculos/vehicles.html', {
        'title': 'Vehículos',
        'vehicles': vehicles
    })
def create_vehicle(request):
    rol = None

    # Si es superuser (admin)
    if request.user.is_authenticated and request.user.is_superuser:
        rol = 'admin'

    form = RegisterVehicle(request.POST or None, request.FILES or None, rol=rol)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('vehiculos')

    return render(request, "pages/vehiculos/crear.html", {
        "form": form
    })
#Editar vehiculos
def edit_vehiculo(request, id):
    instance=Vehiculos.objects.get(idvehiculo=id)

    form = RegisterVehicle(request.POST or None, request.FILES or None, instance= instance)
    if request .method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo editado correctamente")
            return redirect('vehiculos')
            
    return render(request, 'pages/vehiculos/edit.html', {
         'title': 'Editar Vehiculos',
         'form': form 
    })

#Eliminar vehiculos Individual
def delete_vehiculo(request, id):
    device = get_object_or_404(Vehiculos, idvehiculo =id)
    device.delete()
    return redirect("vehiculos")



#acerda de
@login_required(login_url="admin")
def about(request):
    
    return render(request, 'pages/acerca/about.html', {
        'title': 'Acerca de'
    })






