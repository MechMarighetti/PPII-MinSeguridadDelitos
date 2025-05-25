import os
from peewee import *
from playhouse.db_url import connect
from dotenv import load_dotenv

# Cargar variables del entorno desde el .env
load_dotenv()

# Conexión a la base de datos MySQL
db = MySQLDatabase(
    os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT"))
)

class BaseModel(Model):
    class Meta:
        database = db

class Delito(BaseModel):
    id_delito = AutoField()
    expediente = CharField(unique=True, max_length=50)
    nombre_delito = CharField(max_length=100)  # Validación en la API
    fecha_ocurrencia = DateField()
    descripcion = TextField(null=True)
    id_comisaria = IntegerField()
    fecha_registro = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

class Victima(BaseModel):
    id_victima = AutoField()
    genero = CharField(max_length=1)  # 'F', 'M', 'X', 'O'
    fecha_nacimiento = DateField()
    comuna_residencia = IntegerField(constraints=[Check('comuna_residencia BETWEEN 1 AND 15')])
    es_menor = BooleanField()
    id_delito = ForeignKeyField(Delito, backref='victimas', on_delete='CASCADE')

class Usuario(BaseModel):
    id_usuario = AutoField()
    username = CharField(unique=True, max_length=50)
    password_hash = CharField(max_length=255)
    rol = CharField(constraints=[Check("rol IN ('admin', 'editor', 'consulta')")])
    comisaria_asignada = IntegerField(null=True)
    activo = BooleanField(default=True)