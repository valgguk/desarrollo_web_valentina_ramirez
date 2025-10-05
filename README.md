# Aplicación de Adopción de Mascotas — Versión Flask + MySQL

Este repositorio evolucionó desde un prototipo estático (HTML/CSS/JS) hacia una **aplicación Flask** con persistencia en **MySQL** utilizando **SQLAlchemy**. Aquí se documentan los pasos para instalar, ejecutar, poblar datos y los principales criterios de diseño y validación, para facilitar la revisión docente.

---
## 1. Requisitos previos
1. Python 3.10+ (probado con 3.10/3.11)
2. MySQL Server en localhost (se asume credenciales del curso: usuario `cc5002`, password `programacionweb` y base `tarea2`).
3. (Opcional) Git instalado si se clona el repositorio.

---
## 2. Clonar (o descargar) el proyecto
```bash
git clone <URL-del-repo>
cd desarrollo_web_valentina_ramirez
```
Si se descarga como ZIP, simplemente extraer y ubicarse en la carpeta raíz.

---
## 3. Crear y activar entorno virtual (Windows PowerShell)
```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```
Para desactivar: `deactivate`.

---
## 4. Instalar dependencias
```powershell
pip install -r requirements.txt
```
El archivo `requirements.txt` incluye: Flask, Flask_SQLAlchemy, PyMySQL.

---
## 5. Crear/Importar el esquema MySQL ( regiones / comunas )
En MySQL ejecutar (p. ej. desde MySQL Workbench o consola):
```sql
SOURCE ruta/al/archivo/tarea2/tarea2.sql;
```
El script crea las tablas: `region`, `comuna`, `aviso_adopcion`, `foto`, `contactar_por`.

ENUM relevante (tabla `contactar_por`):
```
'whatsapp','telegram','X','instagram','tiktok','otra'
```

---
## 6. Cargar datos maestros ( avisos de ejemplo )
El repositorio incluye un script de “seed” completo (`seed_full.py`) y uno para limpiar (`clear_seed.py`).

Orden recomendado tras importar el esquema (si ya existen datos antiguos de avisos puedes limpiar antes):
```powershell
python clear_seed.py   # elimina avisos, fotos y canales existentes (seguro si parte vacío)
python seed_full.py    # inserta 5 avisos con fotos small+large y canales
```

El seed:
- Copia imágenes desde `app/static/images` hacia `app/static/uploads`.
- Inserta pares de fotos (small `_320x240` + large `_800x600`).
- Ajusta `fecha_ingreso` y `fecha_entrega` con valores definidos para reproducir orden cronológico.
- Usa canales consistentes con el ENUM (`whatsapp`, `instagram`, etc.).

---
## 7. Ejecutar la aplicación
```powershell
python run.py
```
Por defecto: http://127.0.0.1:5000/

Archivos clave:
- `run.py`: punto de entrada.
- `app/__init__.py` (factory `create_app`).
- `app/models.py`: modelos SQLAlchemy.
- `app/routes.py`: rutas (portada, agregar, listado paginado, detalle, estadísticas, API comunas, charts).
- `app/templates/*.html`: vistas Jinja2.
- `app/static/uploads/`: fotos subidas + copiadas por seed.

---
## 8. Flujo de navegación implementado
| Página | Ruta | Descripción |
|--------|------|-------------|
| Portada | `/` | Últimos 5 avisos (filas clickeables + thumbnail con modal). |
| Agregar | `/agregar` | Formulario con validaciones JS + validación servidor. |
| Listado | `/avisos` | Paginación (5 por página). Filas clickeables. |
| Detalle | `/aviso/<id>` | Datos completos + galería (solo miniaturas small; click abre large). |
| Estadísticas | `/estadisticas` | Muestra 3 gráficos estáticos (PNG). |
| API Comunas | `/api/comunas?region_id=<id>` | Devuelve JSON para poblar comunas dinámicamente. |

---
## 9. Validaciones (Cliente y Servidor)
Resumen (se reflejan en JS y en `routes.py`):

Campo | Regla
------|------
Región / Comuna | Ambos obligatorios y la comuna debe pertenecer a la región.
Sector | Opcional, máx 100 caracteres.
Nombre | 3–200 caracteres, obligatorio.
Email | Formato simple regex, máx 100, obligatorio.
Celular | Opcional. Formato `+NNN.NNNNNNNN` (8–12 dígitos tras el punto).
Canales | 0–5. Si se elige vía, identificador 4–50 chars.
Tipo | gato / perro.
Cantidad | Entero ≥ 1.
Edad | Entero ≥ 1.
Unidad | meses → se guarda `m` / años → `a`.
Fecha entrega | `datetime-local`, ≥ ahora+3h (validación cliente) / formato validado servidor.
Fotos | 1–5 imágenes, extensiones en `ALLOWED_IMAGE_EXTENSIONS`.
Descripción | Opcional.

En servidor se replican reglas esenciales para evitar bypass.

---
## 10. Manejo de imágenes
- Upload real: se guarda en `app/static/uploads` usando nombre seguro + prefijo aleatorio.
- Seed: copia archivos de `app/static/images` (no se sobreescriben si ya existen).
- Detalle: solo miniaturas *_320x240 muestran; al click se calcula la versión grande reemplazando sufijo `_320x240` → `_800x600`.
- Portada: mismo patrón (solo primera miniatura). Modal independiente para no interferir con navegación de fila.

---
## 11. Decisiones de diseño destacadas
- No se usa atributo `required`: se fuerza feedback personalizado en cliente.
- Confirmación final mediante `<dialog>` antes de enviar.
- Paginación en servidor (consulta ordenada por `fecha_ingreso desc`).
- Separación chica/large de imágenes para rendimiento (solo miniaturas en listados).
- Se evita dependencia de frameworks JS; solo Vanilla JS.
- Charset `utf8mb4` en la conexión para corregir errores de acentos (reimportación de regiones/comunas se efectuó durante el desarrollo).

---
## 12. Scripts disponibles
| Script | Uso |
|--------|-----|
| `clear_seed.py` | Elimina avisos, fotos y canales (reset). |
| `seed_full.py` | Inserta dataset completo (5 avisos). |
| `normalize_canales.py` | (Opcional) Normaliza ENUM de canales si hubo capitalización anterior. |
| `run.py` | Ejecutar servidor Flask en modo debug. |

---
## 13. Variables/configuración
Archivo: `app/config.py`:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2?charset=utf8mb4"
UPLOAD_FOLDER = "app/static/uploads"
ALLOWED_IMAGE_EXTENSIONS = {"png","jpg","jpeg","gif","webp"}
```
Modificar ahí si cambia usuario/clave o base.

---
## 14. Posibles mejoras futuras
- Base template (`base.html`) para evitar repetición en headers/nav.
- Tests unitarios (por ejemplo usando pytest + Flask testing client).
- Validación de tamaño real de imágenes y compresión.
- Paginación configurable por query param.
- Soporte de internacionalización.
- Reemplazar JS inline del modal por módulo reutilizable.

---
## 15. Licencias
Imágenes de ejemplo: procedentes de Pexels (uso libre). Uso estrictamente educativo.

---
## 16. Ejecución rápida (resumen)
```powershell
git clone <URL>
cd desarrollo_web_valentina_ramirez
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
mysql -u cc5002 -p  # (ejecutar SOURCE tarea2/tarea2.sql dentro de la consola)
python seed_full.py
python run.py
# Navegar a http://127.0.0.1:5000/
```

---
## 18. Contacto
Proyecto académico. Para revisión docente: revisar secciones 9–12 para criterios de corrección.


