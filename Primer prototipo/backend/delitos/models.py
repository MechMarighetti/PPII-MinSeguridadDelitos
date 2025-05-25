from peewee import *
from datetime import datetime, date
from database import db

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    username = CharField(unique=True, max_length=50)
    password_hash = CharField(max_length=255)
    rol = CharField(choices=[('admin', 'admin'), ('editor', 'editor'), ('consulta', 'consulta')])
    comisaria_asignada = IntegerField(null=True)
    activo = BooleanField(default=True)

class Delito(BaseModel):
    expediente = CharField(unique=True, max_length=50)
    nombre_delito = CharField(max_length=100, choices=[
        ('Amenazas', 'Amenazas'),
        ('Lesiones dolosas', 'Lesiones dolosas'),
        ('Otros delitos contra las personas', 'Otros delitos contra las personas'),
        ('Otros delitos contra la integridad sexual', 'Otros delitos contra la integridad sexual'),
        ('Otros delitos contra la libertad', 'Otros delitos contra la libertad'),
        ('Abusos sexuales con acceso carnal', 'Abusos sexuales con acceso carnal'),
        ('Homicidios dolosos', 'Homicidios dolosos'),
        ('Homicidios dolosos en grado de tentativa', 'Homicidios dolosos en grado de tentativa'),
        ('Abuso sexual simple', 'Abuso sexual simple'),
        ('Abuso sexual agravado', 'Abuso sexual agravado')
    ])
    fecha_ocurrencia = DateField()
    descripcion = TextField(null=True)
    id_comisaria = IntegerField()
    fecha_registro = DateTimeField(default=datetime.now)

class Victima(BaseModel):
    genero = CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('X', 'No binario'), ('ND', 'Sin determinar')])
    fecha_nacimiento = DateField()
    comuna_residencia = IntegerField(constraints=[Check('comuna_residencia BETWEEN 1 AND 15')])
    delito = ForeignKeyField(Delito, backref='victimas', on_delete='CASCADE')

    @property
    def es_menor(self):
        """Devuelve True si la víctima era menor al momento del delito."""
        if self.delito:
            edad_en_el_delito = self.delito.fecha_ocurrencia.year - self.fecha_nacimiento.year
            return edad_en_el_delito < 18
        return None