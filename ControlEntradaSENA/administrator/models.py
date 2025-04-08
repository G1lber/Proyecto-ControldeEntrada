# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Centros(models.Model):
    idcentro = models.AutoField(db_column='IdCentro', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreCentro', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'centros'

    def __str__(self):
        return self.nombre


class Dispositivos(models.Model):
    iddispositivo = models.AutoField(db_column='IdDispositivo', primary_key=True)  # Field name made lowercase.
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    sn = models.CharField(db_column='SnDispositivo', unique=True, max_length=50)  # Field name made lowercase.
    tipo = models.ForeignKey('DispositivosTipo', models.DO_NOTHING, db_column='IdTipoDispositivo')  # Field name made lowercase.
    marca = models.ForeignKey('DispositivosMarca', models.DO_NOTHING, db_column='IdMarcaDispositivo')  # Field name made lowercase.
    imagen = models.ImageField(db_column='ImagenDispositivo', upload_to="images/devices/", max_length=50, blank=True, null=True)  # Field name made lowercase.
    documento = models.FileField(db_column='DocumentoDispositivo', upload_to="docs/devices/", max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dispositivos'

    def __str__(self):
        return f"{self.tipo} {self.marca}: #{self.sn[:5]}"


class DispositivosMarca(models.Model):
    idmarcadispositivo = models.AutoField(db_column='IdMarcaDispositivo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreMarcaDispositivo', max_length=20, db_collation='utf8mb4_spanish_ci')  # Field name made lowercase.
    tipo = models.ForeignKey('DispositivosTipo', models.DO_NOTHING, db_column='IdTipoDispositivo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dispositivos_marca'

    def __str__(self):
        return self.nombre


class DispositivosTipo(models.Model):
    idtipodispositivo = models.AutoField(db_column='IdTipoDispositivo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreTipoDispositivo', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dispositivos_tipo'

    def __str__(self):
        return self.nombre


class DocumentoTipo(models.Model):
    idtipodocumento = models.AutoField(db_column='IdTipoDocumento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreTipoDocumento', unique=True, max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'documento_tipo'

    def __str__(self):
        return self.nombre


class Fichas(models.Model):
    idficha = models.AutoField(db_column='IdFicha', primary_key=True)  # Field name made lowercase.
    centro = models.ForeignKey(Centros, models.DO_NOTHING, db_column='IdCentro')  # Field name made lowercase.
    tipo = models.ForeignKey('FichasTipo', models.DO_NOTHING, db_column='IdTipoFicha')  # Field name made lowercase.
    nombre = models.ForeignKey('FichasNombre', models.DO_NOTHING, db_column='IdNombreFicha')  # Field name made lowercase.
    numero = models.CharField(db_column='NumeroFicha', unique=True, max_length=10)  # Field name made lowercase.
    jornada = models.ForeignKey('Jornada', models.DO_NOTHING, db_column='IdJornada')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fichas'
    
    def __str__(self):
        return f"{self.numero}: {self.nombre}"


class FichasNombre(models.Model):
    idfichanombre = models.AutoField(db_column='IdFichaNombre', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreFicha', unique=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fichas_nombre'

    def __str__(self):
        return self.nombre


class FichasTipo(models.Model):
    idtipoficha = models.AutoField(db_column='IdTipoFicha', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreTipoFicha', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fichas_tipo'

    def __str__(self):
        return self.nombre


class Ingresos(models.Model):
    idingreso = models.AutoField(db_column='IdIngreso', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='FechaIngreso')  # Field name made lowercase.
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='IdVehiculo', blank=True, null=True)  # Field name made lowercase.
    dispositivo = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo', related_name='ingresos_set' ,blank=True, null=True)  # Field name made lowercase.
    dispositivo2 = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo2', related_name='ingresos_set2', blank=True, null=True)  # Field name made lowercase.
    dispositivo3 = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo3', related_name='ingresos_set3',blank=True, null=True)  # Field name made lowercase.
    horaingreso = models.TimeField(db_column='HoraIngreso')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ingresos'


class Salidas(models.Model):
    idsalida = models.AutoField(db_column='IdSalida', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='FechaSalida')  # Field name made lowercase.
    ingreso = models.ForeignKey(Ingresos, models.DO_NOTHING, db_column='IdIngreso')  # Field name made lowercase.
    vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='IdVehiculo', blank=True, null=True)  # Field name made lowercase.
    dispositivo = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo', related_name='salidas_set', blank=True, null=True)  # Field name made lowercase.
    dispositivo2 = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo2', related_name='salidas_set2', blank=True, null=True)  # Field name made lowercase.
    dispositivo3 = models.ForeignKey(Dispositivos, models.DO_NOTHING, db_column='IdDispositivo3', related_name='salidas_set3', blank=True, null=True)  # Field name made lowercase.
    horasalida = models.TimeField(db_column='HoraSalida')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salidas'


class Jornada(models.Model):
    idjornada = models.AutoField(db_column='IdJornada', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreJornada', unique=True, max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'jornada'

    def __str__(self):
        return self.nombre


class Roles(models.Model):
    idrol = models.AutoField(db_column='IdRol', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreRol', unique=True, max_length=20)  # Field name made lowercase.
    descripcion = models.TextField(db_column='DescripcionRol')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roles'

    def __str__(self):
        return self.nombre


class Sanciones(models.Model):
    idsancion = models.AutoField(db_column='IdSancion', primary_key=True)  # Field name made lowercase.
    vehiculo = models.ForeignKey('Vehiculos', models.DO_NOTHING, db_column='IdVehiculo')  # Field name made lowercase.
    fecha_inicio = models.DateField(db_column='Fecha_Inicio_Sancion')  # Field name made lowercase.
    fecha_fin = models.DateField(db_column='Fecha_Fin_Sancion')  # Field name made lowercase.
    estado = models.IntegerField(db_column='EstadoSancion')  # Field name made lowercase.
    descripcion = models.TextField(db_column='DescripcionSancion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sanciones'


class Usuarios(models.Model):
    idusuario = models.AutoField(db_column='IdUsuario', primary_key=True)  # Field name made lowercase.
    nombres = models.CharField(db_column='NombresUsuario', max_length=50)  # Field name made lowercase.
    apellidos = models.CharField(db_column='ApellidosUsuario', max_length=50)  # Field name made lowercase.
    tipodocumento = models.ForeignKey(DocumentoTipo, models.DO_NOTHING, db_column='IdTipoDocumento')  # Field name made lowercase.
    documento = models.CharField(db_column='DocumentoUsuario', unique=True, max_length=10)  # Field name made lowercase.
    telefono = models.CharField(db_column='TelefonoUsuario', unique=True, max_length=10)  # Field name made lowercase.
    correo = models.CharField(db_column='CorreoUsuario', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    centro = models.ForeignKey(Centros, models.DO_NOTHING, db_column='IdCentro', blank=True, null=True, default=None)  # Field name made lowercase.
    rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='IdRol')  # Field name made lowercase.
    ficha = models.ForeignKey(Fichas, models.DO_NOTHING, db_column='IdFicha', blank=True, null=True, default=None)  # Field name made lowercase.
    imagen = models.ImageField(db_column='ImagenUsuario', upload_to="images/users/", max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return (f"{self.nombres} {self.apellidos}")
        
    def delete(self, using=None, keep_parents=False):
        # Eliminar la imagen si existe
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super(Usuarios, self).delete(using=using, keep_parents=keep_parents)


class Vehiculos(models.Model):
    idvehiculo = models.AutoField(db_column='IdVehiculo', primary_key=True)  # Field name made lowercase.
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, db_column='IdUsuario')  # Field name made lowercase.
    tipo = models.ForeignKey('VehiculosTipo', models.DO_NOTHING, db_column='IdTipoVehiculo')  # Field name made lowercase.
    placa= models.CharField(db_column='PlacaVehiculo', unique=True, null=True, blank=True, max_length=7, default="000-000")  # Field name made lowercase.
    marca = models.ForeignKey('VehiculosMarca', models.DO_NOTHING, db_column='IdMarcaVehiculo')  # Field name made lowercase.
    modelo = models.CharField(db_column='ModeloVehiculo', null=True, blank=True, max_length=4, default=None)  # Field name made lowercase. This field type is a guess.
    imagen = models.ImageField(db_column='ImagenVehiculo', upload_to="images/vehicles/", max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehiculos'

    def __str__(self):
        return f"{self.tipo} {self.marca}: {self.placa}"


class VehiculosMarca(models.Model):
    idmarcavehiculo = models.AutoField(db_column='IdMarcaVehiculo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreMarcaVehiculo', max_length=20)  # Field name made lowercase.
    tipo = models.ForeignKey('VehiculosTipo', models.DO_NOTHING, db_column='IdTipoVehiculo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehiculos_marca'

    def __str__(self):
        return self.nombre


class VehiculosTipo(models.Model):
    idtipovehiculo = models.AutoField(db_column='IdTipoVehiculo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='NombreTipoVehiculo', unique=True, max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vehiculos_tipo'

    def __str__(self):
        return self.nombre
