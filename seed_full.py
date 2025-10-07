"""Seed completo basado en data.js con fechas exactas y copia de fotos small+large.
Uso:
  (.venv) python clear_seed.py   # limpiar
  (.venv) python seed_full.py    # sembrar
"""
from datetime import datetime
import os, shutil
from app import create_app
from app.models import db, AvisoAdopcion, Comuna, Region, ContactarPor, Foto

DATA = [
    {
        "sector": "Beauchef 850, terraza",
        "tipo": "gato", "cantidad": 1, "edad": 2, "unidad_medida": "m",
        "nombre": "María López", "email": "maria@example.com", "celular": "+569.12345678",
        "region": "Región Metropolitana de Santiago", "comuna": "Santiago",
    "canales": [("whatsapp", "wa.me/56912345678")],
        "fecha_publicacion": "2025-08-18 12:00", "fecha_entrega": "2025-08-25 15:05",
        "descripcion": "gatito cariñoso encontrado en campus",
        "fotos": [
            ("app/static/images/item1_photo1_320x240.png", "item1_photo1_320x240.png"),
            ("app/static/images/item1_photo1_800x600.png", "item1_photo1_800x600.png"),
            ("app/static/images/item1_photo2_320x240.png", "item1_photo2_320x240.png"),
            ("app/static/images/item1_photo2_800x600.png", "item1_photo2_800x600.png")
        ]
    },
    {
        "sector": "Parque Bustamante",
        "tipo": "perro", "cantidad": 2, "edad": 1, "unidad_medida": "a",
        "nombre": "Pedro Pérez", "email": "pedro@example.com", "celular": "+569.23456789",
        "region": "Región Metropolitana de Santiago", "comuna": "Providencia",
    "canales": [("instagram", "instagram.com/pedro")],
        "fecha_publicacion": "2025-08-17 09:30", "fecha_entrega": "2025-08-24 12:35",
        "descripcion": "perritos hermanos, muy juguetones",
        "fotos": [
            ("app/static/images/item2_photo1_320x240.png", "item2_photo1_320x240.png"),
            ("app/static/images/item2_photo1_800x600.png", "item2_photo1_800x600.png"),
            ("app/static/images/item2_photo2_320x240.png", "item2_photo2_320x240.png"),
            ("app/static/images/item2_photo2_800x600.png", "item2_photo2_800x600.png")
        ]
    },
    {
        "sector": "Plaza Ñuñoa",
        "tipo": "gato", "cantidad": 3, "edad": 4, "unidad_medida": "m",
        "nombre": "Valentina R.", "email": "valentina@example.com", "celular": None,
        "region": "Región Metropolitana de Santiago", "comuna": "Ñuñoa",
    "canales": [("telegram", "@valentina")],
        "fecha_publicacion": "2025-08-16 14:45", "fecha_entrega": "2025-08-17 17:47",
        "descripcion": "tres gatitos rescatados",
        "fotos": [
            ("app/static/images/item3_photo1_320x240.png", "item3_photo1_320x240.png"),
            ("app/static/images/item3_photo1_800x600.png", "item3_photo1_800x600.png"),
            ("app/static/images/item3_photo2_320x240.png", "item3_photo2_320x240.png"),
            ("app/static/images/item3_photo2_800x600.png", "item3_photo2_800x600.png")
        ]
    },
    {
        "sector": "Cerro Alegre",
        "tipo": "perro", "cantidad": 1, "edad": 3, "unidad_medida": "a",
        "nombre": "Ana Díaz", "email": "ana@example.com", "celular": "+569.87654321",
        "region": "Región de Valparaíso", "comuna": "Valparaíso",
    "canales": [("X", "x.com/anad")],  # 'X' se mantiene exactamente así (mayúscula)
        "fecha_publicacion": "2025-08-15 11:15", "fecha_entrega": "2025-08-20 15:15",
        "descripcion": "perro adulto esterilizado",
        "fotos": [
            ("app/static/images/item4_photo1_320x240.png", "item4_photo1_320x240.png"),
            ("app/static/images/item4_photo1_800x600.png", "item4_photo1_800x600.png"),
            ("app/static/images/item4_photo2_320x240.png", "item4_photo2_320x240.png"),
            ("app/static/images/item4_photo2_800x600.png", "item4_photo2_800x600.png")
        ]
    },
    {
        "sector": "5 Norte",
        "tipo": "gato", "cantidad": 1, "edad": 8, "unidad_medida": "m",
        "nombre": "Luis F.", "email": "luis@example.com", "celular": None,
        "region": "Región de Valparaíso", "comuna": "Viña del Mar",
    "canales": [("otra", "sitio.luis.cl/adopta")],
        "fecha_publicacion": "2025-08-14 13:20", "fecha_entrega": "2025-08-21 17:20",
        "descripcion": "gato muy tranquilo",
        "fotos": [
            ("app/static/images/item5_photo1_320x240.png", "item5_photo1_320x240.png"),
            ("app/static/images/item5_photo1_800x600.png", "item5_photo1_800x600.png"),
            ("app/static/images/item5_photo2_320x240.png", "item5_photo2_320x240.png"),
            ("app/static/images/item5_photo2_800x600.png", "item5_photo2_800x600.png")
        ]
    },
    {
        "sector": "Fundo Loma Verde",
        "tipo": "perro",
        "cantidad": 2,
        "edad": 5,
        "unidad_medida": "a",
        "nombre": "Andrea Yovany",
        "email": "matcha@gmail.com",
        "celular": "+569.94561234",
        "region": "Región de Valparaíso",
        "comuna": "Algarrobo",
        "canales": [
            ("whatsapp", "wa.me/56994561234"),
            ("instagram", "instagram.com/andrea_lomaverde")
        ],
        "fecha_publicacion": "2025-10-13 10:10",
        "fecha_entrega": "2025-10-24 16:30",
        "descripcion": "2 pastores alemanes grandes, preciosos, bien portados y muy cariñosos. Buscan familia responsable.",
        "fotos": [
            ("app/static/images/item8_photo_1_320x240.png", "item8_photo1_320x240.png"),
            ("app/static/images/item8_photo_1_800x600.png", "item8_photo1_800x600.png"),
            ("app/static/images/item8_photo_2_320x240.png", "item8_photo2_320x240.png"),
            ("app/static/images/item8_photo_2_800x600.png", "item8_photo2_800x600.png"),
            ("app/static/images/item8_photo_3_320x240.png", "item8_photo3_320x240.png"),
            ("app/static/images/item8_photo_3_800x600.png", "item8_photo3_800x600.png"),
            ("app/static/images/item8_photo_4_320x240.png", "item8_photo4_320x240.png"),
            ("app/static/images/item8_photo_4_800x600.png", "item8_photo4_800x600.png"),
            ("app/static/images/item8_photo_5_320x240.png", "item8_photo5_320x240.png"),
            ("app/static/images/item8_photo_5_800x600.png", "item8_photo5_800x600.png")
        ]
    },
    {
        "sector": "Pasaje El Roble",
        "tipo": "gato",
        "cantidad": 1,
        "edad": 1,
        "unidad_medida": "m",
        "nombre": "Sofía Martínez",
        "email": "sofia.martinez@example.com",
        "celular": "+569.77881234",
        "region": "Región del Biobío",
        "comuna": "Concepción",
        "canales": [
            ("telegram", "@sofiagatos")
        ],
        "fecha_publicacion": "2025-08-12 18:40",
        "fecha_entrega": "2025-08-16 12:00",
        "descripcion": "Gatito gris de 1 mes, muy tranquilo y dócil. Ideal para departamento, come sólido blando.",
        "fotos": [
            ("app/static/images/item6_photo_1_320x240.png", "item6_photo1_320x240.png"),
            ("app/static/images/item6_photo_1_800x600.png", "item6_photo1_800x600.png"),
            ("app/static/images/item6_photo_2_320x240.png", "item6_photo2_320x240.png"),
            ("app/static/images/item6_photo_2_800x600.png", "item6_photo2_800x600.png")
        ]
    },
]

def main():
    app = create_app()
    with app.app_context():
        base = os.getcwd()
        upload_dir = os.path.join(base, 'app', 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        inserted = 0
        for item in DATA:
            region = Region.query.filter(Region.nombre.like(f"%{item['region']}%")).first()
            if not region:
                print(f"[WARN] Región no encontrada: {item['region']}")
                continue
            comuna = Comuna.query.filter_by(region_id=region.id, nombre=item['comuna']).first()
            if not comuna:
                print(f"[WARN] Comuna no encontrada: {item['comuna']} ({region.nombre})")
                continue
            fecha_pub = datetime.strptime(item['fecha_publicacion'], "%Y-%m-%d %H:%M")
            fecha_ent = datetime.strptime(item['fecha_entrega'], "%Y-%m-%d %H:%M")
            aviso = AvisoAdopcion(
                comuna_id=comuna.id,
                sector=item['sector'],
                nombre=item['nombre'],
                email=item['email'],
                celular=item['celular'],
                tipo=item['tipo'],
                cantidad=item['cantidad'],
                edad=item['edad'],
                unidad_medida=item['unidad_medida'],
                fecha_entrega=fecha_ent,
                descripcion=item['descripcion']
            )
            aviso.fecha_ingreso = fecha_pub
            db.session.add(aviso)
            db.session.flush()
            for via, ident in item['canales']:
                canal = ContactarPor(nombre=via, identificador=ident, actividad_id=aviso.id)
                db.session.add(canal)
            for src_rel, dest_name in item['fotos']:
                src_abs = os.path.join(base, src_rel)
                dest_abs = os.path.join(upload_dir, dest_name)
                if os.path.exists(src_abs) and not os.path.exists(dest_abs):
                    shutil.copyfile(src_abs, dest_abs)
                if os.path.exists(dest_abs):
                    foto = Foto(ruta_archivo=dest_name, nombre_archivo=dest_name, actividad_id=aviso.id)
                    db.session.add(foto)
                else:
                    print(f"[WARN] Foto origen no encontrada: {src_abs}")
            inserted += 1
        db.session.commit()
        print(f"Insertados {inserted} avisos correctamente.")

if __name__ == '__main__':
    main()
