# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, send_from_directory
from .models import db, AvisoAdopcion, Comuna, Region, Foto, ContactarPor
from sqlalchemy import desc
from datetime import datetime, timedelta
import os, secrets
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename

bp = Blueprint("main", __name__)

def allowed(filename: str, allowed_exts: set[str] | None = None):
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".",1)[-1].lower()
    if allowed_exts is None:
        allowed_exts = set(current_app.config.get("ALLOWED_IMAGE_EXTENSIONS", {"jpg","jpeg","png","gif","webp"}))
    return ext in allowed_exts

def _plural(num: int, singular: str, plural: str):
    return f"{num} {singular if num == 1 else plural}"

def _clean_text(value: str | None, max_len: int):
    if not value:
        return ""
    value = value.strip().replace('\x00','')  # remove stray nulls
    if len(value) > max_len:
        value = value[:max_len]
    return value

@bp.route("/")
def index():
    avisos = (AvisoAdopcion.query
              .order_by(desc(AvisoAdopcion.fecha_ingreso))
              .limit(5)
              .all())
    return render_template("index.html", avisos=avisos, plural=_plural)

@bp.route("/agregar", methods=["GET","POST"])
def agregar():
    regiones = Region.query.order_by(Region.nombre).all()
    # POST
    if request.method == "POST":
        form = request.form
        files = request.files.getlist("fotos[]")
        errores = []

        # Región / Comuna
        region_id = form.get("region_id")
        comuna_id = form.get("comuna_id")
        comuna = Comuna.query.get(comuna_id) if comuna_id else None
        if not comuna or str(comuna.region_id) != region_id:
            errores.append("Comuna/Región inválida.")

        nombre = _clean_text(form.get("nombre"), 200)
        if not (3 <= len(nombre) <= 200):
            errores.append("Nombre: 3-200.")

        email = _clean_text(form.get("email"), 100)
        import re
        if not email or len(email) > 100:
            errores.append("Email requerido <=100.")
        elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            errores.append("Email formato inválido.")

        cel = _clean_text(form.get("cel"), 20)
        if cel and not re.match(r"^\+\d{3}\.\d{8,12}$", cel):
            errores.append("Celular formato inválido.")

        sector = _clean_text(form.get("sector"), 100)
        if len(sector) > 100:
            errores.append("Sector máx 100 caracteres.")

        tipo = form.get("tipo")
        if tipo not in ("gato","perro"):
            errores.append("Tipo inválido.")

        try:
            cantidad = int(form.get("cantidad",""))
            if cantidad < 1:
                raise ValueError()
        except ValueError:
            errores.append("Cantidad inválida.")

        try:
            edad = int(form.get("edad",""))
            if edad < 1:
                raise ValueError()
        except ValueError:
            errores.append("Edad inválida.")

        unidad = form.get("unidad")
        if unidad not in ("meses","años"):
            errores.append("Unidad inválida.")

        fecha_entrega_raw = form.get("fechaEntrega") or form.get("fecha_entrega")
        fecha_entrega = None
        if fecha_entrega_raw:
            try:
                fecha_entrega = datetime.strptime(fecha_entrega_raw.strip(), "%Y-%m-%dT%H:%M")
            except Exception:
                errores.append("Fecha entrega inválida (formato).")
        else:
            errores.append("Fecha entrega inválida (faltante).")
        if fecha_entrega:
            ahora = datetime.now()
            if fecha_entrega < (ahora + timedelta(hours=3)):
                errores.append("Fecha entrega debe ser ≥ ahora + 3 horas.")

        descripcion = _clean_text(form.get("descripcion"), 500)
        if len(descripcion) > 500:
            errores.append("Descripción máx 500 caracteres.")

        vias = request.form.getlist("canal_via[]")
        ids = request.form.getlist("canal_id[]")
        canales = []
        for via, ident in zip(vias, ids):
            via = (via or "").strip()
            ident = (ident or "").strip()
            if via:
                if not (4 <= len(ident) <= 50):
                    errores.append(f"Canal {via}: identificador 4-50.")
                canales.append((via, ident))
        if len(canales) > 5:
            errores.append("Máx 5 canales.")

        allowed_exts = set(current_app.config.get("ALLOWED_IMAGE_EXTENSIONS",
                                                 {"jpg","jpeg","png","gif","webp"}))

        valid_files = [f for f in files if f and f.filename]
        if len(valid_files) == 0:
            errores.append("Al menos 1 foto requerida.")
        if len(valid_files) > 5:
            errores.append("Máx 5 fotos.")
        for f in valid_files:
            filename = f.filename
            ext = filename.rsplit(".",1)[-1].lower() if "." in filename else ""
            mimetype = (f.mimetype or "").lower()

            if not allowed(filename, allowed_exts):
                errores.append(f"Extensión no permitida: {filename}")
                continue
            if ext == "pdf" or "pdf" in mimetype:
                errores.append(f"Archivo no es una imagen válida: {filename}")
                continue
            
            f.stream.seek(0)
            try:
                img_probe = Image.open(f.stream)
                img_probe.verify()
                f.stream.seek(0)
                with Image.open(f.stream) as _tmp:
                    _tmp.load()
            except UnidentifiedImageError:
                errores.append(f"Archivo no es una imagen válida: {filename}")
            except Exception:
                errores.append(f"Error al leer imagen: {filename}")
            finally:
                f.stream.seek(0)

        if errores:
            flash("Hay errores en el formulario.", "error")
            return render_template("agregar.html",
                                   regiones=regiones,
                                   errores=errores,
                                   data=form,
                                   canales=canales)

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
        db.session.flush()

        for via, ident in canales:
            c = ContactarPor(nombre=via, identificador=ident, actividad_id=aviso.id)
            db.session.add(c)

        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        for f in valid_files:
            safe_name = secure_filename(f.filename)
            token = secrets.token_hex(8)
            name_no_ext, ext = os.path.splitext(safe_name)
            img = Image.open(f.stream)
            if ext.lower() in ['.jpg', '.jpeg', '.webp']:
                img = img.convert('RGB')
            sizes = { '_320x240': (320,240), '_800x600': (800,600) }
            for suf, (tw,th) in sizes.items():
                resized = img.copy()
                resized.thumbnail((tw,th))
                canvas = Image.new('RGB', (tw,th), (255,255,255))
                rx, ry = resized.size
                canvas.paste(resized, ((tw-rx)//2, (th-ry)//2))
                variant_filename = f"{token}_{name_no_ext}{suf}{ext.lower()}"
                out_path = os.path.join(upload_dir, variant_filename)
                canvas.save(out_path, quality=90)
                if suf == '_320x240':
                    db.session.add(Foto(ruta_archivo=variant_filename, 
                                        nombre_archivo=safe_name, 
                                        actividad_id=aviso.id))

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
    return render_template("listado.html", page=paginated, plural=_plural)


@bp.route("/aviso/<int:aviso_id>")
def detalle(aviso_id):
    aviso = (AvisoAdopcion.query
             .filter_by(id=aviso_id)
             .first_or_404())
    return render_template("detalle.html", aviso=aviso, plural=_plural)

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