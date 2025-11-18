"""Elimina avisos, fotos, canales y comentarios para re-sembrar limpio.
Uso:
  (.venv) python clear_seed.py
"""
from app import create_app
from app.models import db, AvisoAdopcion, Foto, ContactarPor, Comentario

def main():
    app = create_app()
    with app.app_context():
        # Borrar dependientes primero por integridad (orden importante)
        deleted_comentarios = Comentario.query.delete()
        deleted_fotos = Foto.query.delete()
        deleted_canales = ContactarPor.query.delete()
        deleted_avisos = AvisoAdopcion.query.delete()
        db.session.commit()
        print(f"✅ Eliminados:")
        print(f"   - {deleted_comentarios} comentarios")
        print(f"   - {deleted_fotos} fotos")
        print(f"   - {deleted_canales} canales")
        print(f"   - {deleted_avisos} avisos")

if __name__ == '__main__':
    main()
