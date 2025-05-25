# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('consulta', 'Consulta'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    comisaria_asignada = models.IntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)

class Delito(models.Model):
    TIPO_DELITO = [
        ("Amenazas", "Amenazas"),
        ("Lesiones dolosas", "Lesiones dolosas"),
        ("Otros delitos contra las personas", "Otros delitos contra las personas"),
        ("Otros delitos contra la integridad sexual", "Otros delitos contra la integridad sexual"),
        ("Otros delitos contra la libertad", "Otros delitos contra la libertad"),
        ("Abusos sexuales con acceso carnal", "Abusos sexuales con acceso carnal"),
        ("Homicidios dolosos", "Homicidios dolosos"),
        ("Homicidios dolosos en grado de tentativa", "Homicidios dolosos en grado de tentativa"),
        ("Abuso sexual simple", "Abuso sexual simple"),
        ("Abuso sexual agravado", "Abuso sexual agravado")
    ]
    expediente = models.CharField(max_length=50, unique=True)
    nombre_delito = models.CharField(max_length=100, choices=TIPO_DELITO)
    fecha_ocurrencia = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    id_comisaria = models.IntegerField()
    fecha_registro = models.DateTimeField(default=timezone.now)

class Victima(models.Model):
    GENEROS = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('X', 'No binario'),
        ('S', 'Sin determinar')
    )
    genero = models.CharField(max_length=1, choices=GENEROS)
    fecha_nacimiento = models.DateField()
    comuna_residencia = models.IntegerField()
    id_delito = models.ForeignKey(Delito, on_delete=models.CASCADE)

    @property
    def es_menor(self):
        return self.fecha_nacimiento > (self.id_delito.fecha_ocurrencia - timezone.timedelta(days=365*18))