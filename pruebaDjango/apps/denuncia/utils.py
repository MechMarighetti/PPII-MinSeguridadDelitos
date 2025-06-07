from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
import datetime


def grupo_requerido(nombre_grupo):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            return redirect('login')
        return _wrapped_view
    return decorator



def generar_numero_expediente():
    fecha = datetime.datetime.now()
    return f"EXP-{fecha.strftime('%Y%m%d')}-{fecha.strftime('%H%M%S')}"