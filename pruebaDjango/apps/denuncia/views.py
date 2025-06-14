from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.victima.form import VictimaForm
from .form import DenunciaForm
from apps.victima.models import Victima
from .models import Denuncia
from .models import Delito
from django.db.models import Count
from django.http import JsonResponse
from .utils import *
from .utils import generar_numero_expediente

@login_required 
def registrar_denuncia(request):
    if request.method == 'POST':
        denuncia_form = DenunciaForm(request.POST)
        victima_form = VictimaForm(request.POST)

        if denuncia_form.is_valid() and victima_form.is_valid():
            victima = victima_form.save()
            denuncia = denuncia_form.save(commit=False)
            denuncia.victima = victima
            denuncia.save()
            return redirect('denuncia_exitosa')
    else:
        expediente_generado = generar_numero_expediente()  
        denuncia_form = DenunciaForm(initial={'expediente': expediente_generado})
        victima_form = VictimaForm()

    return render(request, 'denuncia/registrar_denuncia.html', {
        'denuncia_form': denuncia_form,
        'victima_form': victima_form
    })

def grafico_delitos_por_tipo(request):
    
    # Consulta para contar denuncias por tipo de delito
    datos = Denuncia.objects.values('delito__nombre').annotate(total=Count('id')).order_by('-total')
    
    # Preparar datos para Chart.js
    labels = [item['delito__nombre'] for item in datos]
    valores = [item['total'] for item in datos]
    
    return JsonResponse({
        'labels': labels,
        'datos': valores,
        'titulo': 'Denuncias por tipo de delito',
        'tipo': 'polarArea'
    })


    

@login_required
def denuncia_exitosa(request):
    return render(request, 'denuncia/exito.html')


@login_required
def home(request):
    user = request.user
    grupos = user.groups.values_list('name', flat=True)

    contexto = {
        'is_admin': user.is_superuser,
        'is_editor': 'editor' in grupos,
        'is_consulta': 'consulta' in grupos,
    }

    return render(request, 'home.html', contexto)


@grupo_requerido('editor')
def editar_denuncia(request, id):
    denuncia = get_object_or_404(Denuncia, id=id)

    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DenunciaForm(instance=denuncia)

    return render(request, 'editar_denuncia.html', {'form': form})


@login_required
def ver_denuncias(request):
    denuncias = Denuncia.objects.select_related('victima', 'delito').all().order_by('-fecha_registro')
    return render(request, 'denuncia/ver_denuncias.html', {'denuncias': denuncias})
@login_required
def estadisticas(request):
    return render(request, 'denuncia/estadisticas.html')


