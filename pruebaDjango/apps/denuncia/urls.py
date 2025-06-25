from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .form import CustomLoginForm  



urlpatterns = [
    path('home/', views.home, name='home'),

    path('denuncias/registrar/', views.registrar_denuncia, name='registrar_denuncia'),
    path('denuncias/exito/', views.denuncia_exitosa, name='denuncia_exitosa'),

    path('exito/', views.denuncia_exitosa, name='denuncia_exitosa'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=CustomLoginForm
        ), name='login'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    
    path('ver/', views.ver_denuncias, name='ver_denuncias'),
    path('detalle/<int:id>/', views.detalle_denuncia, name='detalle_denuncia'),
    path('editar/<int:id>/', views.editar_denuncia, name='editar_denuncia'),
    path('eliminar/<int:id>/', views.eliminar_denuncia, name='eliminar_denuncia'),
]