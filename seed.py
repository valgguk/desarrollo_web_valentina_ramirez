"""Script de siembra de datos iniciales basado en el antiguo data.js
Crea 5 avisos con canales y sin fotos reales (opcional placeholder).
Ejecutar:
  (.venv) python seed.py
Requiere que la BD tenga regiones/comunas cargadas.
"""
from datetime import datetime, timedelta
from app import create_app
from app.models import db, AvisoAdopcion, Comuna, ContactarPor, Foto

DATA = [
  {
    "sector": "Beauchef 850, terraza",
    "tipo": "gato", "cantidad": 1, "edad": 2, "unidad": "m",
    "nombre": "María López", "email": "maria@example.com", "celular": "+569.12345678",
    "canales": [("whatsapp", "wa.me/56912345678")],
    "descripcion": "gatito cariñoso encontrado en campus"
  },
  {
    "sector": "Parque Bustamante",
    "tipo": "perro", "cantidad": 2, "edad": 1, "unidad": "a",
    "nombre": "Pedro Pérez", "email": "pedro@example.com", "celular": "+569.23456789",
    "canales": [("instagram", "instagram.com/pedro")],
    "descripcion": "perritos hermanos, muy juguetones"
  },
  {
    "sector": "Plaza Ñuñoa",
    "tipo": "gato", "cantidad": 3, "edad": 4, "unidad": "m",
    "nombre": "Valentina R.", "email": "valentina@example.com", "celular": "",
    "canales": [("telegram", "@valentina")],
    "descripcion": "tres gatitos rescatados"
  },
  {
    "sector": "Cerro Alegre",
    "tipo": "perro", "cantidad": 1, "edad": 3, "unidad": "a",
    "nombre": "Ana Díaz", "email": "ana@example.com", "celular": "+569.87654321",
    "canales": [("X", "x.com/anad")],
    "descripcion": "perro adulto esterilizado"
  },
  {
    "sector": "5 Norte",
    "tipo": "gato", "cantidad": 1, "edad": 8, "unidad": "m",
    "nombre": "Luis F.", "email": "luis@example.com", "celular": "",
    "canales": [("otra", "sitio.luis.cl/adopta")],
    "descripcion": "gato muy tranquilo"
  },
]

def main():
    app = create_app()
    with app.app_context():
        # Elegimos una comuna cualquiera (primera) para asignar; si quieres asignar distintas, se podría mapear por región.
        comuna = Comuna.query.first()
        if not comuna:
            print("No hay comunas cargadas. Aborta.")
            return
        now = datetime.utcnow()
        for i, item in enumerate(DATA):
            aviso = AvisoAdopcion(
                comuna_id=comuna.id,
                sector=item["sector"],
                nombre=item["nombre"],
                email=item["email"],
                celular=item["celular"] or None,
                tipo=item["tipo"],
                cantidad=item["cantidad"],
                edad=item["edad"],
                unidad_medida=item["unidad"],
                fecha_entrega=now + timedelta(days=7+i),
                descripcion=item["descripcion"]
            )
            db.session.add(aviso)
            db.session.flush()
            for via, ident in item["canales"]:
                c = ContactarPor(nombre=via, identificador=ident, actividad_id=aviso.id)
                db.session.add(c)
            # Foto placeholder (podrías copiar alguna a uploads manualmente)
            foto = Foto(ruta_archivo="item1_photo1_320x240.png", nombre_archivo="placeholder.png", actividad_id=aviso.id)
            db.session.add(foto)
        db.session.commit()
        print("Insertados", len(DATA), "avisos de prueba.")

if __name__ == "__main__":
    main()
