from django.shortcuts import render, redirect
from apps.victima.form import VictimaForm
from apps.denuncia.form import DenunciaForm

def registrar_denuncia(request):
    if request.method == "POST":
        victima_form = VictimaForm(request.POST)
        denuncia_form = DenunciaForm(request.POST)

        if victima_form.is_valid() and denuncia_form.is_valid():
            victima = victima_form.save()
            denuncia = denuncia_form.save(commit=False)
            denuncia.victima = victima
            denuncia.save()
            return redirect('denuncia_exitosa')  # nombre de la URL a redirigir después

    else:
        victima_form = VictimaForm()
        denuncia_form = DenunciaForm()

    return render(request, 'denuncia/registrar_denuncia.html', {
        'victima_form': victima_form,
        'denuncia_form': denuncia_form
    })

def denuncia_exitosa(request):
    return render(request, 'denuncia/exito.html')

def home(request):
    return render(request, 'home.html')
