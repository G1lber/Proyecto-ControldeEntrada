from django import forms
from django.forms import ModelForm
from administrator.models import Usuarios, DocumentoTipo, Centros, Roles, Fichas, Dispositivos, DispositivosTipo, Vehiculos, VehiculosTipo, DispositivosMarca, VehiculosMarca
from django.core.exceptions import ValidationError
#Fecha y hora
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")


#Formulario para registro de usuario
class RegisterUser(ModelForm):
    class Meta:
        model = Usuarios
        fields = "__all__"

    #Campos
    nombres = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '50', 'autofocus': True}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '50'}))
    tipodocumento = forms.ModelChoiceField(queryset=DocumentoTipo.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), empty_label="Tipo de documento", label="")
    documento = forms.CharField(widget=forms.TextInput(attrs={'onkeypress': 'return valideNumber(event)', 'readonly': True}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '10', 'onkeypress': 'return valideNumber(event)'}))
    correo = forms.EmailField(widget=forms.TextInput(attrs={'maxlength': '50'}))
    centro = forms.ModelChoiceField(queryset=Centros.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), empty_label="Centro", label="")
    rol = forms.ModelChoiceField(queryset=Roles.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'disabled': True}), empty_label="Rol", label="Rol")
    ficha = forms.ModelChoiceField(queryset=Fichas.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), empty_label="Ficha", label="")
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'user-file'}), label="Foto de perfil")

    #Validacion de imagen   
    def clean_imagen(self):  # sourcery skip: extract-method
        imagen_form = self.cleaned_data.get('imagen', False)
        imagen_instance = self.instance.imagen
        imagen = imagen_form or imagen_instance

        documento_instance = self.instance.documento
        documento_form = self.cleaned_data.get('documento')

        if imagen:
            # Verifica que la extensión del archivo sea .jpg, .png o jpeg
            extension = imagen.name.split('.')[-1].lower()
            if extension not in ['jpg', 'png', 'jpeg']:
                raise ValidationError("El archivo debe estar en formato JPG o PNG.")    
            # Elimina la imagen anterior del usuario
            self.instance.imagen.delete()            
            # Usa el valor del campo 'documento' del formulario si está presente, de lo contrario, usa el del instance
            documento = documento_form or documento_instance            
            # Genera el nombre del archivo de imagen y actualiza el atributo 'name' de la imagen
            filename = f"{documento}.{extension}"
            imagen.name = filename

        return imagen
    
    #Validar nombre
    def clean_nombres(self):
        nombre = self.cleaned_data.get('nombres')
        return nombre.title()
    
    def clean_apellidos(self):
        apellido = self.cleaned_data.get('apellidos')
        return apellido.title()
        


#Formulario para registro de dispositivo         
class RegisterDevice(ModelForm):
    class Meta:
        model = Dispositivos
        fields = "__all__"

    #Campos
    usuario = forms.ModelChoiceField(queryset=Usuarios.objects.all(), widget=forms.HiddenInput())
    sn = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 50, 'autofocus': True, 'onkeyup': 'Upper(this)'}), label="Serial Number")
    tipo = forms.ModelChoiceField(queryset=DispositivosTipo.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'tipo'}), label="", empty_label="Tipo de dispositivo")
    marca = forms.ModelChoiceField(queryset=DispositivosMarca.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'single-select-field'}), label="", empty_label="Marca")
    documento = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    #Validacion de imagen
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        usuario = self.cleaned_data['usuario']
        sn = self.cleaned_data['sn']
        if imagen:
            # Verifica que la extensión del archivo sea .jpg o .png
            extension = imagen.name.split('.')[-1].lower()
            if extension not in ['jpg', 'png', 'jpeg']:
                raise ValidationError("El archivo debe estar en formato JPG o PNG.")
            filename = f"{usuario.idusuario}.{sn}.{imagen.name.split('.')[-1]}"
            imagen.name = filename
        return imagen
    
    def clean_doc(self):
        if doc := self.cleaned_data.get('documento', False):
            extension = doc.name.split('.')[-1].lower()
            if extension not in ['pdf']:
                raise ValidationError("El archivo debe estar en formato PDF.")
            tipo = self.cleaned_data['tipo']
            sn = self.cleaned_data['sn']
            marca = self.cleaned_data['marca']
            filename = f"{tipo}-{marca}-{sn}-{doc.name.split('.')[-1]}"
            doc.name = filename
    

#Formulario para registro de vehiculo
class RegisterVehicle(ModelForm):
    
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2023 + 1)]
    YEAR_CHOICES.insert(0, ('', 'Selecciona el modelo'))
    class Meta:
        model = Vehiculos
        fields = "__all__"

    #Campos
    usuario = forms.ModelChoiceField(queryset=Usuarios.objects.all(), widget=forms.HiddenInput(attrs={'readonly': True}), label="")
    tipo = forms.ModelChoiceField(queryset=VehiculosTipo.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), label="", empty_label="Tipo de vehiculo", disabled=True)
    placa = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 7, 'autofocus': True, 'onkeyup': 'Upper(this)'}))
    marca = forms.ModelChoiceField(queryset=VehiculosMarca.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'single-select-field'}), label="", empty_label="Marca")
    modelo = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), label="", choices=YEAR_CHOICES)
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)

    #Validacion de imagen
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        usuario = self.cleaned_data['usuario']
        placa = self.cleaned_data['placa']
        if imagen:
            # Verifica que la extensión del archivo sea .jpg o .png
            extension = imagen.name.split('.')[-1].lower()
            if extension not in ['jpg', 'png', 'jpeg']:
                raise ValidationError("El archivo debe estar en formato JPG o PNG.")
            filename = f"{usuario.idusuario}.{placa}.{imagen.name.split('.')[-1]}"
            imagen.name = filename
        return imagen