"""Elimina avisos, fotos y canales para re-sembrar limpio.
Uso:
  (.venv) python clear_seed.py
"""
from app import create_app
from app.models import db, AvisoAdopcion, Foto, ContactarPor

def main():
    app = create_app()
    with app.app_context():
        # Borrar dependientes primero por integridad
        deleted_fotos = Foto.query.delete()
        deleted_canales = ContactarPor.query.delete()
        deleted_avisos = AvisoAdopcion.query.delete()
        db.session.commit()
        print(f"Eliminados {deleted_fotos} fotos, {deleted_canales} canales, {deleted_avisos} avisos.")

if __name__ == '__main__':
    main()
