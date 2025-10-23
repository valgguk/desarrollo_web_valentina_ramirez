# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify, send_from_directory, session
from .models import db, AvisoAdopcion, Comuna, Region, Foto, ContactarPor, Comentario
from sqlalchemy import desc, func
from datetime import datetime, timedelta
import os, secrets
from PIL import Image, ImageOps, UnidentifiedImageError
from werkzeug.utils import secure_filename
import re
import unicodedata

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

CONTROL_CHARS_RE = re.compile(r'[\x00-\x08\x0B-\x1F\x7F]')
WHITESPACE_RE = re.compile(r'\s+')

def _clean_text(value: str | None, max_len: int, allow_newlines: bool = False):
    if not value:
        return ""
    # Normaliza Unicode (previene trucos con combinaciones)
    value = unicodedata.normalize("NFC", value)
    # Elimina caracteres de control (excepto \n si se permite)
    cleaned = []
    for ch in value:
        if ch in ("\n", "\r"):
            if allow_newlines and ch == "\n":
                cleaned.append("\n")
            continue
        if ord(ch) < 32 or ord(ch) == 127:
            continue
        cleaned.append(ch)
    value = "".join(cleaned)
    # Colapsa espacios
    value = WHITESPACE_RE.sub(" ", value).strip()
    if len(value) > max_len:
        value = value[:max_len]
    return value

def _foto_base_name(fname: str) -> str:
    """
    Elimina sufijos de variante (_large, _small) o dimensiones (_800x600, _320x240)
    antes de la extensión para identificar la 'foto lógica'.
    """
    return re.sub(r'_(?:large|small|\d+x\d+)(?=\.)', '', fname)

@bp.before_app_request
def ensure_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)

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

        # CSRF check
        token_form = request.form.get("csrf_token")
        if not token_form or token_form != session.get("csrf_token"):
            flash("CSRF token inválido.", "error")
            return redirect(url_for("main.agregar"))

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

        # Canales (sanitización + regex)
        canal_vias = request.form.getlist("canal_via[]")
        canal_ids = request.form.getlist("canal_id[]")
        CANAL_VIA_PERMITIDOS = {"whatsapp","telegram","X","instagram","tiktok","otra"}
        CANAL_ID_RE = re.compile(r'^[A-Za-z0-9_.@/+:-]{4,50}$')
        canales_limpios = []
        for via, ident in zip(canal_vias, canal_ids):
            via = _clean_text(via, 15)
            ident = _clean_text(ident, 50)
            if not via or not ident:
                continue
            if via not in CANAL_VIA_PERMITIDOS:
                errores.append(f"Canal '{via}' inválido.")
                continue
            if not CANAL_ID_RE.match(ident):
                errores.append(f"ID canal inválido: {ident}")
                continue
            canales_limpios.append((via, ident))
        if len(canales_limpios) > 5:
            errores.append("Máx 5 canales.")
        # Imágenes reforzadas
        ALLOWED_EXT = {"png","jpg","jpeg","gif","webp"}
        MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
        MAX_DIM = (4000, 4000)

        fotos_validas = []
        for storage in files:
            if not storage or storage.filename == "":
                continue

            filename = secure_filename(storage.filename)
            if "." not in filename:
                errores.append(f"Archivo sin extensión: {filename}")
                continue

            ext_lower = filename.rsplit(".",1)[1].lower()
            if ext_lower not in ALLOWED_EXT:
                errores.append(f"Extensión no permitida: {filename}")
                continue

             # Tamaño (bytes)
            storage.stream.seek(0, 2)  # al final
            size = storage.stream.tell()
            storage.stream.seek(0)
            if size > MAX_FILE_SIZE:
                errores.append(f"Imagen >2MB: {filename}")
                continue

            # Validar formato y dimensiones con Pillow
            try:
                img = Image.open(storage.stream)
                img.verify()  # chequeo rápido
            except (UnidentifiedImageError, OSError):
                errores.append(f"Imagen corrupta o no válida: {filename}")
                storage.stream.seek(0)
                continue

            # Reabrir porque verify deja el archivo en estado no usable
            storage.stream.seek(0)
            with Image.open(storage.stream) as img2:
                if img2.width > MAX_DIM[0] or img2.height > MAX_DIM[1]:
                    errores.append(f"Imagen excede 4000px: {filename}")
                    storage.stream.seek(0)
                    continue

            storage.stream.seek(0)
            fotos_validas.append(storage)

        if len(fotos_validas) == 0:
            errores.append("Al menos 1 foto requerida.")
        if len(fotos_validas) > 5:
            errores.append("Máx 5 fotos.")

        if errores:
            flash("Hay errores en el formulario.", "error")
            return render_template("agregar.html",
                                   regiones=regiones,
                                   errores=errores,
                                   data=form,
                                   canales=canales_limpios)
        # Crear aviso
        aviso = AvisoAdopcion(
            comuna_id=comuna.id,
            fecha_ingreso=datetime.now(), # antes datetime.utcnow()
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

        # Canales
        for via, ident in canales_limpios:
            c = ContactarPor(nombre=via, identificador=ident, actividad_id=aviso.id)
            db.session.add(c)

        # Generación variantes imagen (upscale)
        def generar_variant(img_orig: Image.Image, tw: int, th: int,
                            mode: str = "contain", upscale: bool = True,
                            bg=(255,255,255)):
            if mode == "cover":
                return ImageOps.fit(img_orig, (tw, th), Image.LANCZOS, centering=(0.5,0.5))
            # contain
            w, h = img_orig.size
            ratio_w = tw / w
            ratio_h = th / h
            r = min(ratio_w, ratio_h)
            if r > 1 and not upscale:
                r = 1
            new_w = max(1, int(w * r))
            new_h = max(1, int(h * r))
            img_resized = img_orig.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new("RGB", (tw, th), bg)
            canvas.paste(img_resized, ((tw - new_w)//2, (th - new_h)//2))
            return canvas
        
        MODE = "contain"   # otra opcion : "cover"
        UPSCALE = True
        sizes = {
            "_800x600": (800, 600),
            "_320x240": (320, 240),
        }

        # Guardar imágenes (solo registro small)
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)

        for f in fotos_validas:
            safe_name = secure_filename(f.filename)
            token = secrets.token_hex(8)
            name_no_ext, ext_dot = os.path.splitext(safe_name)
            
            f.stream.seek(0)
            img = Image.open(f.stream)
            if ext_dot.lower() in ('.jpg', '.jpeg', '.webp'):
                img = img.convert('RGB')
            
            for suf, (tw,th) in sizes.items():
                variant_img = generar_variant(img, tw, th,
                                              mode=MODE, upscale=UPSCALE)
                variant_filename = f"{token}_{name_no_ext}{suf}{ext_dot.lower()}"
                out_path = os.path.join(upload_dir, variant_filename)
                variant_img.save(out_path, quality=90)
                if suf == "_320x240":
                    db.session.add(Foto(
                        ruta_archivo=variant_filename,
                        nombre_archivo=safe_name,
                        actividad_id=aviso.id
                    ))

        db.session.commit()
        flash("Aviso agregado exitosamente.", "success")
        return redirect(url_for("main.index"))

    return render_template("agregar.html", regiones=regiones)

@bp.route("/aviso/<int:aviso_id>")
def detalle(aviso_id):
    aviso = (AvisoAdopcion.query
             .filter_by(id=aviso_id)
             .first_or_404())
    return render_template("detalle.html", aviso=aviso, plural=_plural)

@bp.route("/avisos")
@bp.route("/listado")
def listado():
    page_num = request.args.get("page", 1, type=int)
    per_page = 5
    paginated = (AvisoAdopcion.query
                 .order_by(AvisoAdopcion.fecha_ingreso.desc())
                 .paginate(page=page_num, per_page=per_page, error_out=False))

    for aviso in paginated.items:
        unicas = {}
        for foto in aviso.fotos:
            fname = (getattr(foto, 'nombre_archivo', None)
                     or getattr(foto, 'ruta_archivo', None)
                     or getattr(foto, 'filename', '')
                     or '')
            base = _foto_base_name(fname)
            if base not in unicas or ('_800x600' in fname or '_large' in fname):
                unicas[base] = foto
        aviso.fotos_unicas = list(unicas.values())
        aviso.fotos_unicas_count = len(unicas)

    return render_template("listado.html",
                           page=paginated,
                           plural=_plural)


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

# ==================== APIs de Comentarios ====================

@bp.route("/api/comentarios", methods=["POST"])
def api_agregar_comentario():
    """Agregar un comentario a un aviso de adopción"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    # CSRF check
    token = data.get("csrf_token")
    if not token or token != session.get("csrf_token"):
        return jsonify({"error": "CSRF token inválido"}), 403
    
    aviso_id = data.get("aviso_id")
    nombre = _clean_text(data.get("nombre"), 80)
    texto = _clean_text(data.get("texto"), 300, allow_newlines=True)
    
    errores = []
    
    # Validar aviso existe
    aviso = AvisoAdopcion.query.get(aviso_id)
    if not aviso:
        errores.append("Aviso no encontrado")
    
    # Validar nombre (3-80)
    if not nombre or len(nombre) < 3 or len(nombre) > 80:
        errores.append("Nombre: entre 3 y 80 caracteres")
    
    # Validar texto (5-300)
    if not texto or len(texto) < 5 or len(texto) > 300:
        errores.append("Texto: entre 5 y 300 caracteres")
    
    if errores:
        return jsonify({"error": ", ".join(errores)}), 400
    
    # Crear comentario
    comentario = Comentario(
        nombre=nombre,
        texto=texto,
        aviso_id=aviso_id,
        fecha=datetime.now()
    )
    db.session.add(comentario)
    db.session.commit()
    
    return jsonify({
        "id": comentario.id,
        "nombre": comentario.nombre,
        "texto": comentario.texto,
        "fecha": comentario.fecha.strftime("%Y-%m-%d %H:%M:%S")
    }), 201

@bp.route("/api/comentarios/<int:aviso_id>", methods=["GET"])
def api_listar_comentarios(aviso_id):
    """Obtener comentarios de un aviso de adopción"""
    comentarios = (Comentario.query
                   .filter_by(aviso_id=aviso_id)
                   .order_by(Comentario.fecha.desc())
                   .all())
    
    return jsonify([{
        "id": c.id,
        "nombre": c.nombre,
        "texto": c.texto,
        "fecha": c.fecha.strftime("%Y-%m-%d %H:%M:%S")
    } for c in comentarios])

# ==================== APIs de Estadísticas ====================

@bp.route("/api/stats/avisos_por_dia", methods=["GET"])
def api_avisos_por_dia():
    """Gráfico de líneas: avisos por día"""
    resultados = (db.session.query(
        func.date(AvisoAdopcion.fecha_ingreso).label('dia'),
        func.count(AvisoAdopcion.id).label('total')
    )
    .group_by(func.date(AvisoAdopcion.fecha_ingreso))
    .order_by('dia')
    .all())
    
    datos = [{"dia": str(r.dia), "total": r.total} for r in resultados]
    return jsonify(datos)

@bp.route("/api/stats/total_por_tipo", methods=["GET"])
def api_total_por_tipo():
    """Gráfico de torta: total por tipo (gato/perro)"""
    resultados = (db.session.query(
        AvisoAdopcion.tipo,
        func.count(AvisoAdopcion.id).label('total')
    )
    .group_by(AvisoAdopcion.tipo)
    .all())
    
    datos = [{"tipo": r.tipo, "total": r.total} for r in resultados]
    return jsonify(datos)

@bp.route("/api/stats/gatos_perros_por_mes", methods=["GET"])
def api_gatos_perros_por_mes():
    """Gráfico de barras: gatos vs perros por mes"""
    # Usar DATE_FORMAT para MySQL en vez de strftime (SQLite)
    resultados = (db.session.query(
        func.date_format(AvisoAdopcion.fecha_ingreso, '%Y-%m').label('mes'),
        AvisoAdopcion.tipo,
        func.count(AvisoAdopcion.id).label('total')
    )
    .group_by('mes', AvisoAdopcion.tipo)
    .order_by('mes')
    .all())
    
    datos = {}
    for r in resultados:
        mes = r.mes
        if mes not in datos:
            datos[mes] = {"mes": mes, "gatos": 0, "perros": 0}
        if r.tipo == "gato":
            datos[mes]["gatos"] = r.total
        elif r.tipo == "perro":
            datos[mes]["perros"] = r.total
    
    return jsonify(list(datos.values()))
