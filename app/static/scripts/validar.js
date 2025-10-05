
document.addEventListener("DOMContentLoaded", () => {
  // Prefill datetime-local con ahora + 3h solo si el usuario no trajo valor del servidor
  const fechaInput = document.getElementById("fechaEntrega");
  if (fechaInput && !fechaInput.value) {
    const dt = new Date(Date.now() + 3*60*60*1000);
    const toLocalInput = (d) => {
      const pad = (n) => String(n).padStart(2,"0");
      return `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
    };
    fechaInput.value = toLocalInput(dt);
  }

  // Los selects de región y comuna ahora vienen renderizados por el servidor (Jinja + BD)
  const regionSel = document.getElementById("region"); // (opcional dejó manipulación aquí con JS)
  const comunaSel = document.getElementById("comuna");

  // Contact channels dynamic (max 5)
  const canalesDiv = document.getElementById("canales");
  const addCanalBtn = document.getElementById("addCanal");
  function addCanal() {
    const count = canalesDiv.querySelectorAll(".canal").length;
    if (count >= 5) return alert("Máximo 5 canales.");
    const wrap = document.createElement("div");
    wrap.className = "canal";
    wrap.innerHTML = `
      <select class="via" name="canal_via[]">
        <option value="">Seleccione...</option>
        <option value="whatsapp">whatsapp</option>
        <option value="telegram">telegram</option>
        <option value="X">X</option>
        <option value="instagram">instagram</option>
        <option value="tiktok">tiktok</option>
        <option value="otra">otra</option>
      </select>
      <input type="text" class="id" name="canal_id[]" placeholder="ID o URL (4-50)" maxlength="50">
      <button type="button" class="rem">Quitar</button>
    `;
    wrap.querySelector(".rem").addEventListener("click", ()=> wrap.remove());
    canalesDiv.appendChild(wrap);
  }
  addCanalBtn.addEventListener("click", addCanal);

  // Photos dynamic (1 to 5)
  const fotosDiv = document.getElementById("fotos");
  const addFotoBtn = document.getElementById("addFoto");
  function addFoto(){
    const count = fotosDiv.querySelectorAll('input[type="file"]').length;
    if (count >= 5) return alert("Máximo 5 fotos.");
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.name = "fotos[]";
    fotosDiv.appendChild(input);
  }
  addFotoBtn.addEventListener("click", addFoto);
  // Si el servidor no puso ya un input (por error previo), añadimos uno
  if (!fotosDiv.querySelector('input[type="file"]')) {
    addFoto();
  }

  // VALIDATIONS (no "required" attributes; JS only)
  const form = document.getElementById("formAviso");
  const modal = document.getElementById("confirmModal");
  const siBtn = document.getElementById("siSeguro");
  const noBtn = document.getElementById("noSeguro");
  const errores = document.getElementById("errores");
  const erroresWrapper = document.getElementById("erroresClienteWrapper");

  function showErrors(list){
    errores.innerHTML = "";
    list.forEach(e => {
      const li = document.createElement("li");
      li.textContent = e;
      errores.appendChild(li);
    });
    if (erroresWrapper) erroresWrapper.hidden = list.length === 0;
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const err = [];

    // Dónde
    const region = document.querySelector('select[name="region_id"]').value.trim();
    if (!region) err.push("La región es obligatoria.");
    const comuna = document.querySelector('select[name="comuna_id"]').value.trim();
    if (!comuna) err.push("La comuna es obligatoria.");
    const sector = document.getElementById("sector").value.trim();
    if (sector.length > 100) err.push("Sector: largo máximo 100.");

    // Contacto
    const nombre = document.getElementById("nombre").value.trim();
    if (!nombre) err.push("Nombre es obligatorio.");
    if (nombre && (nombre.length < 3 || nombre.length > 200)) err.push("Nombre: entre 3 y 200 caracteres.");
    const email = document.getElementById("email").value.trim();
    if (!email) err.push("Email es obligatorio.");
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email && (!emailRe.test(email) || email.length > 100)) err.push("Email inválido o muy largo (<=100).");
    const cel = document.getElementById("cel").value.trim();
    if (cel) {
      const celRe = /^\+\d{3}\.\d{8,12}$/;
      if (!celRe.test(cel)) err.push("Celular debe ser +NNN.NNNNNNNN (ej: +569.12345678).");
    }

    // Contactar por (opcional, máx 5)
    const canales = Array.from(canalesDiv.querySelectorAll(".canal"));
    if (canales.length > 5) err.push("Máximo 5 canales de contacto.");
    canales.forEach((c,i) => {
      const via = c.querySelector(".via").value;
      const id = c.querySelector(".id").value.trim();
      if (via && (id.length < 4 || id.length > 50)) {
        err.push(`Canal ${i+1}: ID/URL debe tener 4 a 50 caracteres.`);
      }
    });

    // Mascota
    const tipo = document.getElementById("tipo").value;
    if (!tipo) err.push("Debe seleccionar tipo (gato/perro).");
    const cantidad = Number(document.getElementById("cantidad").value);
    if (!Number.isInteger(cantidad) || cantidad < 1) err.push("Cantidad: entero mínimo 1.");
    const edad = Number(document.getElementById("edad").value);
    if (!Number.isInteger(edad) || edad < 1) err.push("Edad: entero mínimo 1.");
    const unidad = document.getElementById("unidad").value;
    if (!unidad) err.push("Debe seleccionar unidad (meses/años).");

    const prefill = fechaInput.value;
    const fechaSel = document.getElementById("fechaEntrega").value;
    if (!fechaSel) err.push("Fecha disponible es obligatoria.");
    // check format yyyy-mm-ddThh:mm (simple check)
    if (fechaSel && !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(fechaSel)) {
      err.push("Fecha disponible: formato inválido (yyyy-mm-ddThh:mm).");
    }
    if (fechaSel && prefill && fechaSel < prefill) {
      err.push("Fecha disponible debe ser >= a la prellenada (ahora + 3h).");
    }

    // Descripción opcional

    // Fotos
    const files = Array.from(fotosDiv.querySelectorAll('input[type="file"]'));
    const hasFoto = files.some(f => f.files && f.files.length > 0);
    if (!hasFoto) err.push("Debe agregar al menos 1 foto.");
    if (files.length > 5) err.push("Máximo 5 fotos.");
    // no need to read files, just count

    showErrors(err);
    if (err.length === 0) {
      // open confirmation
      modal.showModal();
    }
  });

  noBtn.addEventListener("click", ()=> document.getElementById("confirmModal").close());
  siBtn.addEventListener("click", ()=> {
    // En esta versión enviamos realmente el formulario al servidor Flask
    form.submit();
  });
});
