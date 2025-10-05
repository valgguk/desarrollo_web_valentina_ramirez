# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, send_from_directory
from .models import db, AvisoAdopcion, Comuna, Region, Foto, ContactarPor
from sqlalchemy import desc
from datetime import datetime
import os, secrets
from werkzeug.utils import secure_filename

bp = Blueprint("main", __name__)

def allowed(filename):
    ext = filename.rsplit(".",1)[-1].lower()
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]

@bp.route("/")
def index():
    avisos = (AvisoAdopcion.query
              .order_by(desc(AvisoAdopcion.fecha_ingreso))
              .limit(5)
              .all())
    return render_template("index.html", avisos=avisos)

@bp.route("/agregar", methods=["GET","POST"])
def agregar():
    regiones = Region.query.order_by(Region.nombre).all()
    # POST
    if request.method == "POST":
        form = request.form
        files = request.files.getlist("fotos[]")  # ajustaremos name en el form
        errores = []

        # Validaciones servidor (ejemplos, replicaremos las del JS)
        region_id = form.get("region_id")
        comuna_id = form.get("comuna_id")
        comuna = Comuna.query.get(comuna_id) if comuna_id else None
        if not comuna or str(comuna.region_id) != region_id:
            errores.append("Comuna/Región inválida.")

        nombre = (form.get("nombre") or "").strip()
        if not (3 <= len(nombre) <= 200): errores.append("Nombre: 3-200.")

        email = (form.get("email") or "").strip()
        if not email or len(email) > 100: errores.append("Email requerido <=100.")
        # regex simple
        import re
        if email and not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            errores.append("Email formato inválido.")

        cel = (form.get("cel") or "").strip()
        if cel and not re.match(r"^\+\d{3}\.\d{8,12}$", cel):
            errores.append("Celular formato inválido.")

        sector = (form.get("sector") or "").strip()
        if len(sector) > 100: errores.append("Sector máx 100.")

        tipo = form.get("tipo")
        if tipo not in ("gato","perro"): errores.append("Tipo inválido.")

        try:
            cantidad = int(form.get("cantidad",""))
            if cantidad < 1: raise ValueError()
        except ValueError:
            errores.append("Cantidad inválida.")

        try:
            edad = int(form.get("edad",""))
            if edad < 1: raise ValueError()
        except ValueError:
            errores.append("Edad inválida.")

        unidad = form.get("unidad")
        if unidad not in ("meses","años"): errores.append("Unidad inválida.")

        fecha_entrega_raw = form.get("fechaEntrega")
        try:
            fecha_entrega = datetime.strptime(fecha_entrega_raw, "%Y-%m-%dT%H:%M")
        except Exception:
            errores.append("Fecha entrega inválida.")

        descripcion = (form.get("descripcion") or "").strip()

        # Canales dinámicos (se necesita que el form envíe arrays via names tipo canales_via[] / canales_id[])
        vias = request.form.getlist("canal_via[]")
        ids = request.form.getlist("canal_id[]")
        canales = []
        for via, ident in zip(vias, ids):
            via = via.strip()
            ident = (ident or "").strip()
            if via:
                if not (4 <= len(ident) <= 50):
                    errores.append(f"Canal {via}: identificador 4-50.")
                canales.append((via, ident))
        if len(canales) > 5:
            errores.append("Máx 5 canales.")

        # Fotos
        valid_files = [f for f in files if f and f.filename]
        if len(valid_files) == 0:
            errores.append("Al menos 1 foto requerida.")
        if len(valid_files) > 5:
            errores.append("Máx 5 fotos.")
        for f in valid_files:
            if not allowed(f.filename):
                errores.append(f"Extensión no permitida: {f.filename}")

        if errores:
            flash("Hay errores en el formulario.", "error")
            return render_template("agregar.html",
                                   regiones=regiones,
                                   errores=errores,
                                   data=form,
                                   canales=canales)

        # Insert
        aviso = AvisoAdopcion(
            comuna_id=comuna.id,
            sector=sector or None,
            nombre=nombre,
            email=email,
            celular=cel or None,
            tipo=tipo,
            cantidad=cantidad,
            edad=edad,
            unidad_medida="m" if unidad=="meses" else "a",
            fecha_entrega=fecha_entrega,
            descripcion=descripcion or None
        )
        db.session.add(aviso)
        db.session.flush()  # para obtener id

        # Canales
        for via, ident in canales:
            c = ContactarPor(nombre=via, identificador=ident, actividad_id=aviso.id)
            db.session.add(c)

        # Guardar fotos
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        for f in valid_files:
            safe_name = secure_filename(f.filename)
            unique = secrets.token_hex(8) + "_" + safe_name  # evita colisiones
            path = os.path.join(upload_dir, unique)
            f.save(path)
            db.session.add(Foto(ruta_archivo=unique, nombre_archivo=safe_name, actividad_id=aviso.id))

        db.session.commit()
        flash("Aviso agregado exitosamente.", "success")
        return redirect(url_for("main.index"))

    return render_template("agregar.html", regiones=regiones)

@bp.route("/avisos")
def listado():
    page = max(1, int(request.args.get("page", 1)))
    per_page = 5
    paginated = (AvisoAdopcion.query
                 .order_by(AvisoAdopcion.fecha_ingreso.desc())
                 .paginate(page=page, per_page=per_page, error_out=False))
    return render_template("listado.html", page=paginated)


@bp.route("/aviso/<int:aviso_id>")
def detalle(aviso_id):
    aviso = (AvisoAdopcion.query
             .filter_by(id=aviso_id)
             .first_or_404())
    return render_template("detalle.html", aviso=aviso)

@bp.route("/estadisticas")
def estadisticas():
    # Plantilla estática con imágenes de charts; se sirven vía /charts/<file>
    return render_template("estadisticas.html")

@bp.route("/api/comunas")
def api_comunas():
    region_id = request.args.get("region_id", type=int)
    if not region_id:
        return jsonify([])
    comunas = (Comuna.query
               .filter_by(region_id=region_id)
               .order_by(Comuna.nombre)
               .all())
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in comunas])

@bp.route('/charts/<path:filename>')
def charts_static(filename):
    # Sirve archivos de la carpeta raíz 'charts' (una arriba de app.root_path)
    import os
    charts_dir = os.path.join(current_app.root_path, '..', 'charts')
    return send_from_directory(charts_dir, filename)