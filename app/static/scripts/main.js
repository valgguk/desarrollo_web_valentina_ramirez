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
        <td>${item.cantidad} ${item.tipo}${item.cantidad > 1 ? "s" : ""}<br>${item.edad} ${item.unidadEdad}</td>
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
        <td>${a.cantidad} ${a.tipo}${a.cantidad > 1 ? "s" : ""}<br>${a.edad} ${a.unidadEdad}</td>
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
      <h2>Publicación de ${item.nombreContacto}</h2>
      <p><strong>Fecha de publicación:</strong> ${item.fechaPublicacion}</p>
      <p><strong>Fecha de entrega:</strong> ${item.fechaEntrega}</p>
      <p><strong>Región:</strong> ${item.region}</p>
      <p><strong>Comuna:</strong> ${item.comuna}</p>
      <p><strong>Sector:</strong> ${item.sector}</p>
      <p><strong>Cantidad - Tipo - Edad:</strong> 
        ${item.cantidad} ${item.tipo}${item.cantidad > 1 ? "s" : ""},
        ${item.edad} ${item.unidadEdad}
      </p>
      <p><strong>Contacto:</strong> ${item.nombreContacto} — ${item.email} ${item.celular ? " / " + item.celular : ""}</p>
      <p><strong>Canales:</strong> ${item.contactarPor.map(c=>`${c.via}: ${c.id}`).join(", ")}</p>
      <p><strong>Descripción:</strong> ${item.descripcion}</p>
      <div class="galeria">
        ${item.fotos.map((f,i)=>`
          <img 
            src="${f.small}" 
            alt="foto ${i+1}" 
            data-large="${f.large}" 
            width="320" 
            height="240"
            class="foto-chica">
        `).join("")}
      </div>
      <div class="acciones">
        <a href="listado.html"> ← Volver al listado</a>
        <a href="index.html">🏠 Portada</a>
      </div>
    `;

    // Modal de foto
    const modal = document.getElementById("modal-foto");
    const modalImg = document.getElementById("modal-foto-img");
    const cerrarBtn = document.getElementById("cerrar-modal");

    document.querySelectorAll(".foto-chica").forEach(img => {
      img.addEventListener("click", () => {
        modal.classList.add("visible");
        modalImg.src = img.dataset.large; 
      });
    });

    cerrarBtn.addEventListener("click", () => {
      modal.classList.remove("visible");
    });

    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        modal.classList.remove("visible");
      }
    });
  }
});
