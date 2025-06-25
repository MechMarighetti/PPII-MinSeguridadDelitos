from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.victima.form import VictimaForm
from .form import DenunciaForm
from apps.victima.models import Victima
from .models import Denuncia, Delito
from django.db.models import Count, Q
from django.http import JsonResponse
from .utils import grupo_requerido, generar_numero_expediente
from django.core.paginator import Paginator



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


@login_required
def detalle_denuncia(request, id):
    denuncia = get_object_or_404(Denuncia, id=id)
    user = request.user
    grupos = user.groups.values_list('name', flat=True)

    return render(request, 'denuncia/detalle_denuncia.html', {
        'denuncia': denuncia,
        'is_admin': user.is_superuser,
        'is_editor': 'editor' in grupos,
    })

@grupo_requerido('editor')
def editar_denuncia(request, id):
    denuncia = get_object_or_404(Denuncia, id=id)

    if request.method == 'POST':
        form = DenunciaForm(request.POST, instance=denuncia)
        if form.is_valid():
            form.save()
            return redirect('detalle_denuncia', id=denuncia.id)
    else:
        form = DenunciaForm(instance=denuncia)

    return render(request, 'denuncia/editar_denuncia.html', {
        'form': form,
        'denuncia': denuncia,
    })


@login_required
def ver_denuncias(request):
    cantidad = request.GET.get('cantidad', 10)
    busqueda = request.GET.get('buscar', '').strip()

    denuncias_lista = Denuncia.objects.select_related('victima', 'delito')

    if busqueda:
        if busqueda.isdigit():
            denuncias_lista = denuncias_lista.filter(
                Q(id=int(busqueda)) |
                Q(expediente__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(comisaria__icontains=busqueda) |
                Q(delito__nombre__icontains=busqueda)
            )
        else:
            denuncias_lista = denuncias_lista.filter(
                Q(expediente__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(comisaria__icontains=busqueda) |
                Q(delito__nombre__icontains=busqueda)
            )

    denuncias_lista = denuncias_lista.order_by('-fecha_registro')
    paginator = Paginator(denuncias_lista, cantidad)
    pagina = request.GET.get('page')
    denuncias = paginator.get_page(pagina)

    return render(request, 'denuncia/ver_denuncias.html', {
        'denuncias': denuncias,
        'cantidad': int(cantidad),
        'buscar': busqueda,
    })


@login_required
def estadisticas(request):
    grupos = request.user.groups.values_list('name', flat=True)
    return render(request, 'denuncia/estadisticas.html', {
        'is_admin': request.user.is_superuser,
        'is_editor': 'editor' in grupos,
        'is_consulta': 'consulta' in grupos,
    })

@login_required
def grafico_delitos_por_tipo(request):
    datos = Denuncia.objects.values('delito__nombre').annotate(total=Count('id')).order_by('-total')

    labels = [item['delito__nombre'] for item in datos]
    valores = [item['total'] for item in datos]

    return JsonResponse({
        'labels': labels,
        'datos': valores,
        'titulo': 'Denuncias por tipo de delito',
        'tipo': 'polarArea'
    })

@user_passes_test(lambda u: u.is_superuser)
def eliminar_denuncia(request, id):
    denuncia = get_object_or_404(Denuncia, id=id)

    if request.method == 'POST':
        denuncia.delete()
        return redirect('ver_denuncias')

    return render(request, 'denuncia/confirmar_eliminacion.html', {
        'denuncia': denuncia
    })
