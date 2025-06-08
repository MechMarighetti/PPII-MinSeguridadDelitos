"""
URL configuration for delitoApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from apps.denuncia import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('denuncias/', include('apps.denuncia.urls')),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    path('', lambda request: redirect('login', permanent=False)),
    
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('api/grafico-delitos/', views.grafico_delitos_por_tipo, name='grafico_delitos'),
]
