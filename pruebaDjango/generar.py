import os
import django
import random
from faker import Faker
from django.utils import timezone
from django.db import connection

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "delitoApp.settings")
django.setup()

from apps.denuncia.models import Denuncia, Delito
from apps.victima.models import Victima

fake = Faker('es_ES')

# 🔁 Resetear tablas
def reset_tabla(model):
    model.objects.all().delete()
    with connection.cursor() as cursor:
        table = model._meta.db_table
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")  # SQLite
    print(f"🧹 Tabla {model.__name__} limpiada y reiniciada.")

# 👤 Crear víctima compatible con el modelo
def crear_victima():
    return Victima.objects.create(
        genero=random.choices(
            ["F", "M", "X", "S"],
            weights=[0.55, 0.43, 0.12, 0.03]  # Mayor probabilidad para "F", menor para "X"
        )[0],
        fecha_nacimiento=fake.date_of_birth(minimum_age=7, maximum_age=67),
        comuna_residencia=random.randint(1, 15)
    )

# 📋 Diccionario de delitos con descripciones realistas
delitos_con_descripciones = {
    "amenazas": [
        "La víctima recibió amenazas verbales en la vía pública por parte de un vecino.",
        "Se registraron mensajes intimidatorios enviados por redes sociales.",
        "El denunciante fue amenazado telefónicamente tras una discusión laboral."
    ],
    "lesiones dolosas": [
        "La víctima fue golpeada en un conflicto barrial, provocándole heridas leves.",
        "El agresor utilizó un objeto contundente durante la pelea, causando cortes.",
        "Se produjo una pelea en un local nocturno con lesiones visibles en el rostro."
    ],
    "abuso sexual simple": [
        "La víctima denunció tocamientos sin consentimiento en un transporte público.",
        "Durante una fiesta, una persona realizó insinuaciones y contacto físico no deseado.",
        "El hecho ocurrió en una plaza donde el agresor se abalanzó sobre la víctima."
    ],
    "trata de personas": [
        "Se denunció el intento de traslado de una menor con fines de explotación.",
        "Una mujer relató haber sido captada mediante engaños para fines laborales forzados.",
        "El operativo en un domicilio detectó posibles víctimas de trata en situación de vulnerabilidad."
    ],
    "abuso de autoridad": [
        "Un funcionario público excedió sus funciones y retuvo a un civil sin justificación.",
        "Se denunció el uso de violencia por parte de un agente en un procedimiento.",
        "El denunciante refiere amenazas durante un operativo policial injustificado."
    ],
    "tentativa de homicidio": [
        "La víctima logró escapar tras un intento de ataque con arma blanca.",
        "Un testigo declaró que el agresor disparó sin llegar a impactar.",
        "Se denunció un intento de atropello intencional en la vía pública."
    ],
    "violencia familiar": [
        "Se registraron episodios de violencia verbal y física dentro del hogar.",
        "La víctima denunció golpes recibidos por parte de su pareja.",
        "Intervino personal policial ante gritos y ruidos denunciados por vecinos."
    ],
}

def generar_datos(cantidad=500):
    reset_tabla(Denuncia)
    reset_tabla(Victima)

    print("📌 Verificando delitos...")
    for nombre in delitos_con_descripciones:
        Delito.objects.get_or_create(nombre=nombre)
    print(f"✔️ Se aseguraron {len(delitos_con_descripciones)} tipos de delito.")

    print("🛠 Generando denuncias...")


    for delito_nombre, descripciones in delitos_con_descripciones.items():
        delito = Delito.objects.get(nombre=delito_nombre)
        descripcion = random.choice(descripciones)
        victima = crear_victima()

        Denuncia.objects.create(
            victima=victima,
            delito=delito,
            expediente=fake.unique.bothify("EXP-####-????"),
            fecha_ocurrencia=fake.date_between(start_date="-6M", end_date="today"),
            descripcion=descripcion,
            comisaria=str(random.randint(1, 15)),
            fecha_registro=timezone.now()
        )

    restantes = max(0, cantidad - len(delitos_con_descripciones))
    for _ in range(restantes):
        delito_nombre = random.choices(
            population=list(delitos_con_descripciones.keys()),
            weights=[
            3 if k in ["lesiones dolosas", "amenazas"] else 1
            for k in delitos_con_descripciones.keys()
            ]
        )[0]
        descripcion = random.choice(delitos_con_descripciones[delito_nombre])
        delito = Delito.objects.get(nombre=delito_nombre)
        victima = crear_victima()

        Denuncia.objects.create(
            victima=victima,
            delito=delito,
            expediente=fake.unique.bothify("EXP-####-????"),
            fecha_ocurrencia=fake.date_between(start_date="-6M", end_date="today"),
            descripcion=descripcion,
            comisaria=str(random.randint(1, 15)),
            fecha_registro=timezone.now()
        )

    print("✅ Carga completa. Todos los delitos representados al menos una vez.")


if __name__ == "__main__":
    generar_datos(500)
