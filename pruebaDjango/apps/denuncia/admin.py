from django.contrib import admin
from apps.denuncia import models

@admin.register(models.Delito)
class DelitoAdmin(admin.ModelAdmin):
    list_display = ['id','nombre']
    search_fields = ['nombre']

@admin.register(models.Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['id','delito', 'expediente', 'victima__genero', 'fecha_registro', 'comisaria']
    search_fields = ['comisaria', 'delito__nombre']
    list_filter = ['delito__nombre', 'fecha_ocurrencia', 'fecha_registro', 'comisaria']