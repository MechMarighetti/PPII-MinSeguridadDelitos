from django.urls import path
from . import views

urlpatterns = [
    # Ruta a la vista de inicio de denuncias, podría eliminarse si ya se usa en urls.py general
    path('home/', views.home, name='home'),

    # Ruta para registrar una denuncia
    path('registrar/', views.registrar_denuncia, name='registrar_denuncia'),

    # Ruta que se muestra al completar con éxito el registro
    path('exito/', views.denuncia_exitosa, name='denuncia_exitosa'),
]