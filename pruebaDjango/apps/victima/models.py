from django.db import models
from django.utils import timezone

class Victima(models.Model):

    GENEROS = (
    ('F', 'Femenino'),
    ('M', 'Masculino'),
    ('X', 'No binario'),
    ('S', 'Sin determinar')
    
)
    COMUNAS = [(i, f"Comuna {i}") for i in range(1, 16)] 
    genero = models.CharField(max_length=30, choices=GENEROS)
    fecha_nacimiento = models.DateField()
    comuna_residencia = models.PositiveIntegerField(choices=COMUNAS)

    def __str__(self):
        return f"Victima {self.genero}"
