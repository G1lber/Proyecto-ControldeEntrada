from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.db import connection
from .forms import *

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
    initial = {'imagen': instance.imagen}
    form = RegisterUser(request.POST or None, request.FILES or None, instance=instance, initial=initial)

    form.fields['imagen'].required = False
    form.fields['centro'].required = False if instance.rol == 3 else True
    form.fields['ficha'].required = False if instance.rol != 2 else True

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

    form = RegisterDevices(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha registrado correctamente")
            return redirect('dispositivo')
    
    return render(request, 'pages/dispositivos/devices.html', {
        'title': 'Dispositivos',
        'dispositivos': devices,
        'form': form
    })

#Editar dispositivo
def edit_dispositivo(request, id):
    instance = Dispositivos.objects.get(iddispositivo=id)

    form = RegisterDevices(request.POST or None, request.FILES or None, instance= instance)
    if request .method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, "se ha editado correctamente")
            return redirect('dispositivo')
        
    return render(request, 'pages/dispositivos/edit.html', {
        'title': 'Editar dispositivo',
        'form': form
    })



###

#Sanciones
@login_required(login_url="admin")
def sanciones(request):
    sanciones = Sanciones.objects.all()
    
    return render(request, 'pages/sanciones/sanciones.html', {
        'title': 'Sanciones',
        'penaltys': sanciones
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
    vehicles = Vehiculos.objects.all()
    
    return render(request, 'pages/vehiculos/vehicles.html', {
        'title': 'Vehiculos',
        'vehicles': vehicles
    })

#Editar vehiculos
def edit_vehiculo(request, id):
    instance=Vehiculos.objects.get(idvehiculo=id)

    form = RegisterVehicles(request.POST or None, request.FILES or None, instance= instance)
    if request .method == "POST" :
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo editado correctamente")
            return redirect('vehiculos')
            
    return render(request, 'pages/vehiculos/edit.html', {
         'title': 'Editar Vehiculos',
         'form': form 
    })




#acerda de
@login_required(login_url="admin")
def about(request):
    
    return render(request, 'pages/acerca/about.html', {
        'title': 'Acerca de'
    })






