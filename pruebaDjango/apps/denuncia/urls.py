from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from apps.denuncia.form import CustomLoginForm  # o desde donde lo importes realmente



urlpatterns = [
    # Ruta a la vista de inicio de denuncias, podría eliminarse si ya se usa en urls.py general
    path('home/', views.home, name='home'),

    # Ruta para registrar una denuncia
    path('registrar/', views.registrar_denuncia, name='registrar_denuncia'),

    # Ruta que se muestra al completar con éxito el registro
    path('exito/', views.denuncia_exitosa, name='denuncia_exitosa'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomLoginForm
    ), name='login'),
]