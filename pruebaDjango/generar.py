import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Configurar entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delitoApp.settings")
django.setup()

from apps.victima.models import Victima
from apps.denuncia.models import Delito, Denuncia

faker = Faker('es_AR')

def generar_victimas(n=400):
    generos = ['F', 'M', 'X', 'S']
    comunas = list(range(1, 16))

    for _ in range(n):
        fecha_nacimiento = faker.date_between(start_date='-80y', end_date='-18y')

        Victima.objects.create(
            genero=random.choice(generos),
            fecha_nacimiento=fecha_nacimiento,
            comuna_residencia=random.choice(comunas)
        )
    print(f"Se crearon {n} víctimas correctamente.")


def generar_denuncias(n=400):
    delitos = list(Delito.objects.all())
    victimas = list(Victima.objects.all())

    if not delitos or not victimas:
        print(" No hay delitos o víctimas en la base de datos.")
        return

    for _ in range(n):
        delito = random.choice(delitos)
        victima = random.choice(victimas)
        expediente = faker.unique.bothify(text='EXP####-####')
        fecha_ocurrencia = faker.date_between(start_date='-1y', end_date='today')
        descripcion = faker.sentence(nb_words=12)
        comisaria = random.randint(1, 15)

        Denuncia.objects.create(
            delito=delito,
            victima=victima,
            expediente=expediente,
            fecha_ocurrencia=fecha_ocurrencia,
            descripcion=descripcion,
            comisaria=comisaria
        )
    print(f"Se crearon {n} denuncias correctamente.")

if __name__ == "__main__":
    generar_victimas()
    generar_denuncias()
