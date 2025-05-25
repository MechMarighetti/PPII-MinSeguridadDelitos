from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Date, Text, ForeignKey, Boolean, CheckConstraint, DateTime, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from passlib.context import CryptContext
import datetime
import jwt

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
