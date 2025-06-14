from django.shortcuts import render
from apps.victima.models import Victima
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from datetime import date
from django.views.decorators.http import require_GET

@login_required
# Create your views here.
def grafico_victimas_por_genero(request):
    
    # Consulta para contar víctimas por género
    datos = Victima.objects.values('genero').annotate(total=Count('id')).order_by('genero')
    
    # Preparar datos para Chart.js
    labels = [item['genero'] for item in datos]
    valores = [item['total'] for item in datos]
    
    return JsonResponse({
        'labels': labels,
        'datos': valores,
        'titulo': 'Víctimas por género',
        'tipo': 'doughnut'  
    })

@require_GET
@login_required
def grafico_victimas_por_edad(request):
    # Obtener todas las víctimas con fecha de nacimiento
    victimas = Victima.objects.exclude(fecha_nacimiento__isnull=True)
    
    # Calcular edades y clasificar
    edades = []
    mayores = 0
    menores = 0
    
    for victima in victimas:
        hoy = date.today()
        edad = hoy.year - victima.fecha_nacimiento.year - (
            (hoy.month, hoy.day) < (victima.fecha_nacimiento.month, victima.fecha_nacimiento.day)
        )
        edades.append(edad)
        if edad >= 18:
            mayores += 1
        else:
            menores += 1
    
    # Agrupar por edad y contar
    conteo_edades = {}
    for edad in edades:
        conteo_edades[edad] = conteo_edades.get(edad, 0) + 1
    
    # Ordenar por edad
    edades_ordenadas = sorted(conteo_edades.items())
    
    # Preparar datos para el gráfico
    labels = [f"{edad} años" for edad, _ in edades_ordenadas]
    datos = [conteo for _, conteo in edades_ordenadas]
    
    return JsonResponse({
        'labels': labels,
        'datos': datos,
        'titulo': 'Distribución de Víctimas por Edad',
        'tipo': 'line',
        'mayores_edad': mayores,
        'menores_edad': menores,
        'total_victimas': len(victimas)
    })