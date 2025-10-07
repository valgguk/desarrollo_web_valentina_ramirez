# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Region(db.Model):
    __tablename__ = "region"
    id = db.Column(db.Integer, primary_key=True)
    # El dump SQL no declara unique constraint explícito; quitamos unique=True para evitar divergencias
    nombre = db.Column(db.String(200), nullable=False)
    comunas = db.relationship("Comuna", back_populates="region")

class Comuna(db.Model):
    __tablename__ = "comuna"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("region.id"), nullable=False)
    region = db.relationship("Region", back_populates="comunas")
    avisos = db.relationship("AvisoAdopcion", back_populates="comuna")

class AvisoAdopcion(db.Model):
    __tablename__ = "aviso_adopcion"
    id = db.Column(db.Integer, primary_key=True)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now, nullable=False) # antes utcnow
    comuna_id = db.Column(db.Integer, db.ForeignKey("comuna.id"), nullable=False)
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    tipo = db.Column(db.Enum("gato","perro", name="tipo_enum"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Enum("a","m", name="unidad_medida_enum"), nullable=False)  # años=a, meses=m
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text)  # limitar en validación a 500 caracteres
    comuna = db.relationship("Comuna", back_populates="avisos")
    fotos = db.relationship("Foto", back_populates="aviso", cascade="all, delete-orphan", foreign_keys='Foto.actividad_id')
    canales = db.relationship("ContactarPor", back_populates="aviso", cascade="all, delete-orphan", foreign_keys='ContactarPor.actividad_id')

class Foto(db.Model):
    __tablename__ = "foto"
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)   # path relativo
    nombre_archivo = db.Column(db.String(300), nullable=False)
    # En el esquema se llama actividad_id pero referencia a aviso_adopcion.id
    actividad_id = db.Column(db.Integer, db.ForeignKey("aviso_adopcion.id"), nullable=False)
    aviso = db.relationship("AvisoAdopcion", back_populates="fotos")

class ContactarPor(db.Model):
    __tablename__ = "contactar_por"
    id = db.Column(db.Integer, primary_key=True)
    # Enum según esquema original del profesor: 'whatsapp','telegram','X','instagram','tiktok','otra'
    # Mantener exactamente estos valores para evitar LookupError.
    nombre = db.Column(db.Enum('whatsapp','telegram','X','instagram','tiktok','otra', name="canal_enum"), nullable=False)
    identificador = db.Column(db.String(150), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey("aviso_adopcion.id"), nullable=False)
    aviso = db.relationship("AvisoAdopcion", back_populates="canales")