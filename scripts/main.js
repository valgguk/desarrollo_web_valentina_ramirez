// Home & List behaviors
document.addEventListener("DOMContentLoaded", () => {
  // --- Últimos 5 avisos (en tabla) ---
  const lastTable = document.querySelector("#ultimos tbody");
  if (lastTable) {
    // Tomar los últimos 5
    const ultimos = ADOPCIONES.slice(-5).reverse();

    ultimos.forEach(item => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${item.fechaPublicacion}</td>
        <td>${item.comuna}</td>
        <td>${item.sector}</td>
        <td>${item.cantidad} ${item.tipo}<br>${item.edad} ${item.unidadEdad}</td>
        <td><img src="${item.fotos?.[0]?.small || item.foto || ""}" alt="foto" width="80"></td>
      `;

      lastTable.appendChild(tr);
    });
  }

  // --- Tabla general en listado.html ---
  const tabla = document.getElementById("tabla-adopciones");
  if (tabla) {
    // Build table rows
    const tbody = tabla.querySelector("tbody");
    ADOPCIONES.forEach(a => {
      const tr = document.createElement("tr");
      tr.tabIndex = 0;
      tr.setAttribute("role","link");
      tr.addEventListener("click", () => {
        go(`detalle.html?id=${encodeURIComponent(a.id)}`);
      });
      tr.innerHTML = `
        <td>${a.fechaPublicacion}</td>
        <td>${a.fechaEntrega}</td>
        <td>${a.comuna}</td>
        <td>${a.sector}</td>
        <td>${a.cantidad} ${a.tipo}<br>${a.edad} ${a.unidadEdad}</td>
        <td>${a.nombreContacto} — ${a.email}${a.celular ? + a.celular : ""}</td>
        <td>${a.fotos.length}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  // --- Detalle page ---
  const detalleDiv = document.getElementById("detalle");
  if (detalleDiv) {
    const params = new URLSearchParams(window.location.search);
    const id = Number(params.get("id"));
    const item = ADOPCIONES.find(x => x.id === id) || ADOPCIONES[0];
    detalleDiv.innerHTML = `
      <h2>Publicación ${item.publicacion}</h2>
      <p><strong>Fecha:</strong> ${item.fechaPublicacion}</p>
      <p><strong>Entrega:</strong> ${item.region}</p>
      <p><strong>Comuna:</strong> ${item.comuna}</p>
      <p><strong>Sector:</strong> ${item.sector}</p>
      <p><strong>Cantidad:</strong> ${item.cantidad}</p>
      <p><strong>Tipo:</strong> ${item.tipo}</p>
      <p><strong>Edad:</strong> ${item.edad} ${item.unidadEdad}</p>
      <p><strong>Contacto:</strong> ${item.nombreContacto} — ${item.email} ${item.celular ? " / " + item.celular : ""}</p>
      <p><strong>Canales:</strong> ${item.contactarPor.map(c=>`${c.via}: ${c.id}`).join(", ")}</p>
      <p><strong>Descripción:</strong> ${item.descripcion}</p>
      <div class="galeria">
        ${item.fotos.map((f,i)=>`
          <img src="${f.small}" alt="foto ${i+1}" data-large="${f.large}" width="320" height="240">
        `).join("")}
      </div>
      <div class="acciones">
        <a href="listado.html">← Volver al listado</a>
        <a href="index.html">🏠 Portada</a>
      </div>
      <div id="overlay" class="overlay" hidden>
        <div class="overlay-inner">
          <button id="cerrarOverlay" class="btn">Cerrar ✖</button>
          <img id="overlayImg" alt="foto grande" width="800" height="600">
        </div>
      </div>
    `;
    const overlay = document.getElementById("overlay");
    const overlayImg = document.getElementById("overlayImg");
    const cerrar = document.getElementById("cerrarOverlay");
    document.querySelectorAll(".galeria img").forEach(img => {
      img.addEventListener("click", () => {
        overlayImg.src = img.dataset.large;
        overlay.hidden = false;
      });
    });
    cerrar.addEventListener("click", () => overlay.hidden = true);
    overlay.addEventListener("click", (e) => { if (e.target.id === "overlay") overlay.hidden = true; });
  }
});
