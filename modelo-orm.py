from fastapi import FastAPI, HTTPException, Depends

"""
FastApi: Clase principal para crear la aplicación web.
HTTPException: Permite lanzar errores HTTP personalizados (como 404, 401, etc.)
Depends: Se usa para inyectar dependencias como sesiones de base de datos o validación de autenticación. 
"""

from fastapi.middleware.cors import CORSMiddleware

"""
CORSMiddleware: Middleware que permite controlar políticas de CORS (Cross-Origin Resource Sharing). Es útil cuando el frontend (React) y el backend están en dominios diferentes.
"""

from fastapi.security import OAuth2PasswordRequestForm

"""
OAuth2PasswordRequestForm: Clase para manejar formularios de login que usan OAuth2 con contraseña. Extrae username y password del formulario automáticamente. 
"""

from pydantic import BaseModel

"""
Pydantic: Librería de Python que permite definir modelos de datos utilizando anotaciones de tipo, y automáticamente valida y transforma los datos según estas anotaciones.
BaseModel: Clase base de Pydantic para definir modelos de datos con validación automática (por ejemplo, datos que llegan del frontend).
"""

from typing import List, Optional

"""
Typing: Módulo de Python que permite declarar tipos de variables complejas, parámetros de funciones y valores de retorno.
List: Para declarar listas tipadas, por ejemplo: List[int]
Optional: Para indicar que un campo puede ser None (opcional).
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ForeignKey, Boolean, CheckConstraint, DateTime, func

"""
sqlalchemy: Biblioteca de Python que permite interactuar con bases de datos relacionales.
create_engine: Crea la conexión a la base de datos.
Column: Define una columna en una tabla.
Tipos como Integer, String, Date, Text, Boolean, etc., indican el tipo de dato de cada columna.
ForeignKey: Relación entre tablas (clave foránea).
CheckConstraint: Restricciones (como comuna BETWEEN 1 AND 15).
DateTime: Fecha y hora.
func: Permite usar funciones SQL como NOW() desde Python.
"""

from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

"""
declarative_base: Clase base para declarar modelos de datos con SQLAlchemy.
relationship: Define relaciones entre modelos (uno a muchos, etc.).
sessionmaker: Creador de sesiones para interactuar con la base de datos.
Session: Tipo de objeto de sesión que representa una transacción con la base de datos.
"""

from passlib.context import CryptContext

"""
passlib: Biblioteca de Python utilizada para la gestión segura de contraseñas, incluyendo la generación y verificación de hashes.
CryptContext: Proporciona hashing seguro de contraseñas. Se suele usar con bcrypt o argon2 para guardar contraseñas de forma segura.
"""

import datetime

"""
datetime: Módulo de Python para trabajar con fechas y horas.
"""

import jwt

"""
jwt: Biblioteca para codificar y decodificar JSON Web Tokens (JWT), utilizados para autenticar usuarios.
"""

DATABASE_URL = "mysql+mysqlconnector://usuario:password@localhost:3306/seguridad_ciudad"
SECRET_KEY = "clave_secreta"
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), CheckConstraint("rol IN ('admin', 'editor', 'consulta')"), nullable=False)
    comisaria_asignada = Column(Integer)
    activo = Column(Boolean, default=True)

class Delito(Base):
    __tablename__ = "delitos"
    id_delito = Column(Integer, primary_key=True, index=True)
    expediente = Column(String(50), unique=True, nullable=False)
    nombre_delito = Column(String(100), nullable=False)
    fecha_ocurrencia = Column(Date, nullable=False)
    descripcion = Column(Text)
    id_comisaria = Column(Integer)
    fecha_registro = Column(DateTime, default=func.now())

class Victima(Base):
    __tablename__ = "victimas"
    id_victima = Column(Integer, primary_key=True, index=True)
    genero = Column(String(1), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    comuna_residencia = Column(Integer, CheckConstraint("comuna_residencia BETWEEN 1 AND 15"))
    es_menor = Column(Boolean)
    id_delito = Column(Integer, ForeignKey("delitos.id_delito", ondelete="CASCADE"))

Base.metadata.create_all(bind=engine)

class TokenResponse(BaseModel):
    token: str
    rol: str
    comisaria: Optional[int]

def verificar_usuario(username: str, password: str, db: Session):
    usuario = db.query(Usuario).filter(Usuario.username == username, Usuario.activo == True).first()
    if not usuario or not pwd_context.verify(password, usuario.password_hash):
        return None
    return usuario

@app.post("/auth/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    usuario = verificar_usuario(form_data.username, form_data.password, db)
    if not usuario:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token_data = {"sub": usuario.username, "rol": usuario.rol, "comisaria": usuario.comisaria_asignada}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return TokenResponse(token=token, rol=usuario.rol, comisaria=usuario.comisaria_asignada)
