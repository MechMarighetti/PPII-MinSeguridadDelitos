from django.contrib import admin

from apps.victima import models

@admin.register(models.Victima)
class VictimaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'genero', 'comuna_residencia']
    search_fields = ['genero']
    list_filter = ['genero', 'comuna_residencia', 'fecha_nacimiento']
