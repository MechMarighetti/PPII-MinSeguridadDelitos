from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('consulta', 'Consulta'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)
    comisaria_asignada = models.PositiveIntegerField(null=True, blank=True)
    activo = models.BooleanField(default=True)
