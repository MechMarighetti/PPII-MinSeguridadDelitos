from django.db import models
from django.utils import timezone

class Delito(models.Model):

    TIPO_DELITO = (
        ("amenazas", "Amenazas"),
        ("lesiones dolosas", "Lesiones dolosas"),
        ("otros delitos contra las personas", "Otros delitos contra las personas"),
        ("otros delitos contra la integridad sexual", "Otros delitos contra la integridad sexual"),
        ("otros delitos contra la libertad", "Otros delitos contra la libertad"),
        ("abusos sexuales con acceso carnal", "Abusos sexuales con acceso carnal"),
        ("homicidios dolosos", "Homicidios dolosos"),
        ("homicidios dolosos en grado de tentativa", "Homicidios dolosos en grado de tentativa"),
        ("abuso sexual simple", "Abuso sexual simple"),
        ("abuso sexual agravado", "Abuso sexual agravado"),    
    )

    nombre = models.CharField(max_length=100, choices=TIPO_DELITO)

    def __str__(self):
        return self.nombre

class Denuncia(models.Model):
    COMISARIAS = [(i, f"Comisaría {i}") for i in range(1, 16)]

    delito = models.ForeignKey("denuncia.Delito", on_delete=models.CASCADE, related_name="denuncia")
    victima = models.ForeignKey("victima.Victima", on_delete=models.CASCADE, related_name="denuncia")
    expediente = models.CharField(max_length=50, unique=True)
    fecha_ocurrencia = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    comisaria = models.PositiveIntegerField(choices=COMISARIAS)
    fecha_registro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} {self.delito} {self.comisaria} {self.fecha_registro}"


    
