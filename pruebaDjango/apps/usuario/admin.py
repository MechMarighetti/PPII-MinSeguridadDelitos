from django.contrib import admin

from apps.usuario import models

@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id','rol','activo']
    search_fields = ['activo']
