# Prototipo — Gestión de adopción (HTML/CSS/JS)

Este repositorio contiene un **prototipo** de la aplicación solicitada: portada, formulario de aviso, listado, detalle y estadísticas.

## Cómo abrir
No requiere servidor. Basta con abrir `index.html` en su navegador.

## Páginas
- `index.html`: portada con menú y últimos 5 avisos.
- `agregar.html`: formulario con **validaciones en JS** (no usa `required`).
- `listado.html`: tabla con 5 filas inventadas. Al hacer clic, navega al detalle.
- `detalle.html`: muestra todos los datos del aviso y una galería con zoom a 800x600.
- `estadisticas.html`: tres gráficos **estáticos** (imágenes PNG).

## Validaciones clave
- Región/comuna: menús dependientes. Región y comuna obligatorias.
- Sector: opcional, máx 100.
- Nombre: obligatorio (3–200).
- Email: obligatorio, formato válido, máx 100.
- Celular: opcional, formato `+NNN.NNNNNNNN` (ej: `+569.12345678`).
- Contactar por: hasta 5 entradas; si se indica **vía**, el **ID/URL** debe tener 4–50 chars.
- Tipo: obligatorio (gato/perro).
- Cantidad y edad: enteros ≥ 1.
- Unidad edad: obligatorio (meses/años).
- Fecha entrega: `datetime-local`, prellenado a **ahora + 3h**; valor seleccionado ≥ prellenado.
- Fotos: mínimo 1, máximo 5. Botón “agregar otra foto” para añadir inputs.

## Notas de corrección
- HTML5/CSS3 limpios y semánticos
- Sin almacenamiento: al confirmar el envío, solo muestra el mensaje final y botón a la portada.

## Licencias
Todas las imagenes son obtenidas desde Pexels permitido para uso gratuito público. 

