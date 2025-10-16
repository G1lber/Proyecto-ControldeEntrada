from django import forms
from django_select2.forms import ModelSelect2TagWidget
from django.forms import ModelForm
from administrator.models import Usuarios, DocumentoTipo, Centros, Roles, Fichas, Dispositivos, DispositivosTipo, Vehiculos, VehiculosTipo, DispositivosMarca, VehiculosMarca, Jornada, Centros, FichasTipo, FichasNombre, FichasXAprendiz, Extras
from django.core.exceptions import ValidationError
#Fecha y hora
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")
#Para convertir un select en un buscar
from django_select2.forms import Select2Widget

#Formulario para registro de usuario
class RegisterUser(ModelForm):
    class Meta:
        model = Usuarios
        fields = "__all__"

    # Campos personalizados
    nombres = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '50', 'autofocus': True}))
    apellidos = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '50'}))
    tipodocumento = forms.ModelChoiceField(
        queryset=DocumentoTipo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Tipo de documento",
        label=""
    )
    documento = forms.CharField(  # 🔧 sin readonly aquí
        widget=forms.TextInput(attrs={
            'onkeypress': 'return valideNumber(event)'
        })
    )
    telefono = forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': '10',
        'onkeypress': 'return valideNumber(event)'
    }))
    correo = forms.EmailField(widget=forms.TextInput(attrs={
        'maxlength': '50',
        'class': 'form-control'
    }))
    centro = forms.ModelChoiceField(
        queryset=Centros.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Centro",
        label=""
    )
    rol_hide = forms.ModelChoiceField(queryset=Roles.objects.all(), widget=forms.HiddenInput())
    rol = forms.ModelChoiceField(
        queryset=Roles.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'disabled': True}),
        empty_label="Rol",
        label="Rol"
    )
    ficha = forms.ModelChoiceField(
        queryset=Fichas.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Ficha",
        label=""
    )

    def __init__(self, *args, **kwargs):
        self.usuario_actual = kwargs.pop('usuario_actual', None)  # ✅ extraer desde kwargs
        super().__init__(*args, **kwargs)

        # Solo permitir editar documento si es superusuario
        if not (self.usuario_actual and self.usuario_actual.is_superuser):
            self.fields['documento'].widget.attrs['readonly'] = True
        else:
            self.fields['documento'].widget.attrs.pop('readonly', None)

        # ✅ Si el rol es 1 o 3, ficha no obligatoria
        rol_obj = None
        if getattr(self.instance, 'rol', None):
            rol_obj = getattr(self.instance.rol, 'idrol', None)
        elif 'rol' in self.initial and self.initial['rol']:
            rol_value = self.initial['rol']
            rol_obj = getattr(rol_value, 'idrol', rol_value)

        if rol_obj in [1, 3]:
            self.fields['ficha'].required = False

    # ✅ Validación de imagen obligatoria y renombrada
    def clean_imagen(self):
        imagen_form = self.cleaned_data.get('imagen')
        documento_form = self.cleaned_data.get('documento')
        documento_instance = self.instance.documento

        if not imagen_form:
            raise ValidationError("Este campo es obligatorio.")

        extension = imagen_form.name.split('.')[-1].lower()
        if extension not in ['jpg', 'png', 'jpeg']:
            raise ValidationError("El archivo debe estar en formato JPG o PNG.")

        if self.instance.imagen:
            self.instance.imagen.delete()

        documento = documento_form or documento_instance
        filename = f"{documento}.{extension}"
        imagen_form.name = filename

        return imagen_form

    # ✅ Validación de nombres y apellidos
    def clean_nombres(self):
        nombre = self.cleaned_data.get('nombres')
        return nombre.title()

    def clean_apellidos(self):
        apellido = self.cleaned_data.get('apellidos')
        return apellido.title()

    # ✅ Validación final: ficha obligatoria solo si rol ≠ 1 o 3
    def clean(self):
        cleaned_data = super().clean()

        # Detectar el rol desde el formulario o el input oculto del HTML
        rol = cleaned_data.get('rol') or cleaned_data.get('rol_hide')

        # Si viene como número desde el input <input type="hidden" name="rol">
        if not rol and 'rol' in self.data:
            try:
                rol_id = int(self.data.get('rol'))
            except (TypeError, ValueError):
                rol_id = None
        else:
            rol_id = getattr(rol, 'idrol', None)

        ficha = cleaned_data.get('ficha')

        # Solo exigir ficha si el rol NO es instructor (1) ni visitante (3)
        if rol_id not in [1, 3] and not ficha:
            self.add_error('ficha', "La ficha es obligatoria para este rol.")
        else:
            # Si el rol es 1 o 3, permitir ficha vacía
            self.fields['ficha'].required = False

        return cleaned_data

#Formulario para registro de dispositivo         
class RegisterDevice(ModelForm):
    class Meta:
        model = Dispositivos
        fields = "__all__"

    #Campos
    usuario = forms.ModelChoiceField(queryset=Usuarios.objects.all(), widget=Select2Widget(attrs={'class': 'form-control', 'data-placeholder': 'Buscar usuario...'}))
    sn = forms.CharField(widget=forms.TextInput(attrs={'maxlength': 50, 'autofocus': True, 'onkeyup': 'Upper(this)'}), label="Serial Number")
    tipo = forms.ModelChoiceField(queryset=DispositivosTipo.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'tipo'}), label="", empty_label="Tipo de dispositivo")
    marca = forms.ModelChoiceField(queryset=DispositivosMarca.objects.all(), widget=forms.Select(attrs={'class': 'form-select', 'id': 'single-select-field'}), label="", empty_label="Marca")
    # documento = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}))
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'device-file'}), required=False)

    #Validacion de imagen
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        usuario = self.cleaned_data.get('usuario')  # 👈 Aquí lo defines
        sn = self.cleaned_data.get('sn')

        if imagen:
            extension = imagen.name.split('.')[-1].lower()
            if extension not in ['jpg', 'png', 'jpeg']:
                raise ValidationError("El archivo debe estar en formato JPG o PNG.")

            if usuario:
                filename = f"{usuario.idusuario}.{sn}.{extension}"
                imagen.name = filename

        return imagen
    
    # def clean_doc(self):
    #     if doc := self.cleaned_data.get('documento', False):
    #         extension = doc.name.split('.')[-1].lower()
    #         if extension not in ['pdf']:
    #             raise ValidationError("El archivo debe estar en formato PDF.")
    #         tipo = self.cleaned_data['tipo']
    #         sn = self.cleaned_data['sn']
    #         marca = self.cleaned_data['marca']
    #         filename = f"{tipo}-{marca}-{sn}-{doc.name.split('.')[-1]}"
    #         doc.name = filename
    

#Formulario para registro de vehiculo
class RegisterVehicle(ModelForm):
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2023 + 1)]
    YEAR_CHOICES.insert(0, ('', 'Selecciona el modelo'))

    class Meta:
        model = Vehiculos
        fields = "__all__"

    # Campos
    usuario = forms.ModelChoiceField(
        queryset=Usuarios.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=""
    )
    tipo = forms.ModelChoiceField(
        queryset=VehiculosTipo.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="",
        empty_label="Tipo de vehiculo",
        required=True  # Requerido para admin
    )
    placa = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': 7, 'autofocus': True, 'onkeyup': 'Upper(this)'})
    )
    marca = forms.ModelChoiceField(
        queryset=VehiculosMarca.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'single-select-field'}),
        label="",
        empty_label="Marca"
    )
    modelo = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="",
        choices=YEAR_CHOICES
    )
    imagen = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'vehicle-file'}),
        required=False
    )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        rol = kwargs.pop('rol', '').lower()
        tipo_vehiculo_id = kwargs.get('initial', {}).get('tipo')

        super().__init__(*args, **kwargs)

        # Filtrar las marcas según el tipo de vehículo
        if tipo_vehiculo_id:
           self.fields['marca'].queryset = VehiculosMarca.objects.filter(tipo_id=tipo_vehiculo_id)
        else:
            self.fields['marca'].queryset = VehiculosMarca.objects.none()

        # Reglas de roles
        if rol == 'instructor':
            self.fields['tipo'].disabled = True
            self.fields['tipo'].initial = VehiculosTipo.objects.get(nombre="Carro")
        elif rol == 'aprendiz':
            self.fields['tipo'].disabled = True
            self.fields['tipo'].initial = VehiculosTipo.objects.get(nombre="Moto")
        elif rol == 'admin':
            self.fields['tipo'].disabled = False


    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen', False)
        usuario = self.cleaned_data['usuario']
        placa = self.cleaned_data['placa']
        if imagen:
            extension = imagen.name.split('.')[-1].lower()
            if extension not in ['jpg', 'png', 'jpeg']:
                raise ValidationError("El archivo debe estar en formato JPG o PNG.")
            filename = f"{usuario.idusuario}.{placa}.{extension}"
            imagen.name = filename
        return imagen
class FichasNombreWidget(ModelSelect2TagWidget):
    model = FichasNombre
    search_fields = ['nombre__icontains']

    def create_value(self, value):
        # Esto se llama cuando no encuentra una opción y se crea una nueva
        return self.get_queryset().create(nombre=value)

class RegisterFicha(forms.ModelForm):
    nombre = forms.ModelChoiceField(
        queryset=FichasNombre.objects.all(),
        widget=forms.Select(attrs={
            'id': 'id_nombre',
            'class': 'form-select'
        })
    )
    jornada = forms.ModelChoiceField(
        queryset=Jornada.objects.all(),
        empty_label="Seleccione jornada",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo = forms.ModelChoiceField(
        queryset=FichasTipo.objects.all(),
        empty_label="Seleccione tipo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    centro = forms.ModelChoiceField(
        queryset=Centros.objects.all(),
        empty_label="Seleccione centro",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Fichas
        fields = "__all__"
        widgets = {
            'numero': forms.TextInput(attrs={"minlength": "6"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si hay una instancia, asumimos que es edición
        if self.instance and self.instance.pk:
            # Campos deshabilitados
            self.fields['nombre'].disabled = True
            self.fields['tipo'].disabled = True
            self.fields['numero'].widget.attrs['readonly'] = True

            # Para que no rompa la validación
            self.fields['nombre'].required = False
            self.fields['tipo'].required = False

class CargarUsers(forms.ModelForm):
    ficha = forms.ModelChoiceField(
        queryset= Fichas.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_ficha'}),
        to_field_name="idficha",  # Esto asegura que Django use el ID internamente
        required=False
    )
    class Meta:
        model = FichasXAprendiz
        fields = ['ficha', 'aprendiz']

    def __init__(self, *args, **kwargs):
        super(CargarUsers, self).__init__(*args, **kwargs)
        # Deshabilitar el campo ficha manualmente siempre
        self.fields['ficha'].widget.attrs['disabled'] = True


class ExtrasForm(forms.ModelForm):
    class Meta:
        model = Extras
        fields = ['descripcion', 'foto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'id_extra'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        foto = cleaned_data.get('foto')

        if descripcion and not foto:
            self.add_error('foto', 'Debe subir una foto si ha escrito una descripción.')
