# Aplicación de Adopción de Mascotas 

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
El archivo `requirements.txt` incluye: Flask, Flask_SQLAlchemy, PyMySQL, Pillow (para generar miniaturas y versiones large al subir nuevas fotos).

---
## 5. Crear/Importar el esquema MySQL ( regiones / comunas )
Antes de importar el script SQL, se debe de tener un servidor MySQL corriendo y crear la base de datos y el usuario que usa la aplicación (por defecto en este repositorio usamos `cc5002` / `programacionweb` y la base `tarea2`).

Pasos recomendados (PowerShell / Windows):

1. Iniciar el servicio MySQL (si no está corriendo):

```powershell
# desde PowerShell con privilegios de administrador
Start-Service MySQL
# o el nombre del servicio que tengas instalado (MySQL80, mysql, mariadb, ...)
```

2. Conectarse al cliente MySQL (usa una cuenta con permisos para crear bases/usuarios, p. ej. root):

```powershell
mysql -u root -p
```

3. Dentro del cliente `mysql`, crear la base y el usuario (usa UTF8MB4):

```sql
-- crear la base con collation utf8mb4
CREATE DATABASE IF NOT EXISTS tarea2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- crear/actualizar usuario (ejemplo con contraseña del curso)
CREATE USER IF NOT EXISTS 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
```

4. Salir del cliente root y conectarse con el usuario `cc5002` para ejecutar el script (o usar Workbench):

```powershell
mysql -u cc5002 -p tarea2
-- dentro del cliente mysql:
SOURCE ruta/al/archivo/tarea2/tarea2.sql;
```

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tarea2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER IF NOT EXISTS 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb'; GRANT ALL ON tarea2.* TO 'cc5002'@'localhost'; FLUSH PRIVILEGES;"
mysql -u cc5002 -p tarea2 -e "SOURCE C:/ruta/completa/a/tarea2/tarea2.sql;"


```

5. Importar regiones/comunas en Windows (problemas de codificación y solución)
- Problema común: PowerShell y el cliente pueden interpretar distintas codificaciones; usar `Get-Content | mysql` puede re‑codificar el texto y producir mojibake (ej. "Regi├â┬│n"). Solución fiable: preservar los bytes del archivo y forzar UTF‑8 en el cliente MySQL.

Pasos recomendados (rápido, PowerShell):

a) (Opcional, limpiar previo)
```powershell
mysql -u cc5002 -p -e "USE tarea2; SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE comuna; TRUNCATE TABLE region; SET FOREIGN_KEY_CHECKS=1;"
```

b) Copiar el SQL a una ruta sin espacios (evita problemas con OneDrive/espacios):
```powershell
New-Item -Path C:\temp -ItemType Directory -Force
Copy-Item "C:\Users\<usuario>\OneDrive\Documentos\uni\app web\desarrollo_web_valentina_ramirez\tarea2\region-comuna.sql" -Destination "C:\temp\region-comuna.sql" -Force
```

c) Importar preservando bytes (cmd redirection) y forzando utf8mb4:
```powershell
# desde PowerShell invocamos cmd para usar la redirección clásica <
cmd /c "mysql --default-character-set=utf8mb4 -u cc5002 -p tarea2 < C:\temp\region-comuna.sql"
```

d) Alternativa (cliente interactivo desde la carpeta del repo):
```powershell
Set-Location "C:\Users\<usuario>\OneDrive\Documentos\uni\app web\desarrollo_web_valentina_ramirez"
mysql -u cc5002 -p tarea2
# dentro del cliente mysql>:
SET NAMES utf8mb4;
SOURCE tarea2/region-comuna.sql;
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
Descripción | Opcional, máx 500 caracteres.

En servidor se replican reglas esenciales para evitar bypass.

---
## 10. Manejo de imágenes
- Upload real: al subir, el servidor genera automáticamente DOS variantes usando Pillow: `*_320x240` (miniatura) y `*_800x600` (large). Se centra la imagen en un lienzo blanco manteniendo proporción (letterboxing si hace falta). Solo la variante `320x240` se registra en la tabla `foto`; la grande se infiere reemplazando sufijo.
- Seed: copia archivos de `app/static/images` hacia `app/static/uploads` (ya vienen con ambos tamaños en el dataset inicial de ejemplo).
- Detalle / Portada / Listado: solo se cargan miniaturas; al click se abre modal con la grande (reemplazo de sufijo `_320x240` por `_800x600`).

---
## 11. Decisiones de diseño destacadas
- No se usa atributo `required`: se fuerza feedback personalizado en cliente.
- Confirmación final mediante `<dialog>` antes de enviar.
- Paginación en servidor (consulta ordenada por `fecha_ingreso desc`).
- Separación chica/large de imágenes para rendimiento (solo miniaturas en listados).
- Helper de pluralización en backend (`plural(n, singular, plural)`) evita casos como "1 gatos" o "1 meses" (ahora "1 gato", "1 mes").
- Mensajes flash de éxito aparecen superpuestos (overlay) y se desvanecen automáticamente tras ~3.5s.
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
## 14. Licencias
Imágenes de ejemplo: procedentes de Pexels (uso libre). Uso estrictamente educativo.

---
## 15. Ejecución rápida (resumen)
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
## 16. Validación HTML (W3C)
Al validar directamente los archivos de plantilla Jinja aparecían “errores” como:

Bad value {{ url_for('static', filename='styles/styles.css') }} … Illegal character '{'

Estos no corresponden al HTML real; el validador recibe las llaves de Jinja porque el archivo no fue renderizado por Flask. Se deja constancia de que los avisos iniciales eran falsos positivos propios del uso de plantillas.

---
## 17. Contacto
Proyecto académico. Para revisión docente: revisar secciones 9–12 para criterios de corrección.

---
## 18. Tarea 4 - Sistema de Evaluación (Spring Boot)

### Requisitos adicionales
- Java 17+
- Maven 3.6+

### Iniciar aplicación completa (Flask + Spring Boot)

#### Opción 1: Script automático (recomendado)
```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Iniciar ambas aplicaciones
python start_all.py
```

#### Opción 2: Manual (ventanas separadas)
```powershell
# Terminal 1: Flask
.\.venv\Scripts\Activate.ps1
python run.py

# Terminal 2: Spring Boot
cd adopcion-mascotas
.\mvnw.cmd spring-boot:run
```

### URLs de acceso
- **Flask (Tareas 1-3)**: http://127.0.0.1:5000/
- **Spring Boot (Tarea 4)**: http://localhost:8080/evaluacion

### Funcionalidad Tarea 4
- Listado de avisos con promedio de evaluaciones
- Slider interactivo para seleccionar nota entre 1 y 7
- Actualización asíncrona del promedio sin recargar página
- Validación cliente/servidor de rango de notas

### Decisión de diseño - Evaluaciones múltiples

**Implementación actual (para demostración académica):**
- Un usuario puede evaluar el mismo aviso múltiples veces
- Cada nueva nota se agrega a la base de datos y el promedio se recalcula
- Esto permite al evaluador docente verificar el correcto funcionamiento del cálculo de promedios

**Implementación recomendada para producción:**
- Agregar tabla `usuario` con autenticación
- Relacionar cada nota con un `usuario_id`
- Restricción: Un usuario solo puede tener UNA nota por aviso
- Al evaluar nuevamente, se actualiza la nota existente (no se crea una nueva)
- Esto evita manipulación del promedio y refleja la opinión real de cada usuario

**Cambio necesario en producción:**
```sql
-- Agregar constraint único
ALTER TABLE nota ADD CONSTRAINT unique_usuario_aviso UNIQUE (usuario_id, aviso_id);

-- Modificar lógica de inserción para usar UPSERT (INSERT ... ON DUPLICATE KEY UPDATE)
```

---
## 19. Tecnologías por tarea

| Tarea | Stack |
|-------|-------|
| 1-2 | Flask + SQLAlchemy + MySQL + Jinja2 |
| 3 | Flask + Highcharts + Fetch API |
| 4 | Spring Boot + JPA + Thymeleaf + Fetch API |


