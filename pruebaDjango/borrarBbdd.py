import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delitoApp.settings")
django.setup()

from apps.victima.models import Victima
from apps.denuncia.models import Denuncia, Delito

Victima.objects.all().delete()
Denuncia.objects.all().delete()
Delito.objects.all().delete()

print("Base de datos vaciada correctamente.")