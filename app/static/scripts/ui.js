
// Simple helpers for rendering and navigation
function $(sel, ctx=document){ return ctx.querySelector(sel); }
function $all(sel, ctx=document){ return Array.from(ctx.querySelectorAll(sel)); }
function go(url){ window.location.href = url; }
// Mostrar hint al escribir en campos 
const campos = [
  'nombre', 'email', 'tipo', 'cantidad', 'edad', 'unidad', 'fechaEntrega',
  'region', 'comuna', 'sector', 'fotos', 'cel', 'canales', 'descripcion'
];
campos.forEach(id => {
  const input = document.getElementById(id);
  const hint = document.getElementById('hint-' + id);
  if (input && hint) {
    // Para fotos y canales, usa mouseenter/mouseleave
    if (id === 'fotos' || id === 'canales') {
      input.addEventListener('mouseenter', () => {
        hint.style.display = 'inline';
      });
      input.addEventListener('mouseleave', () => {
        hint.style.display = 'none';
      });
    } else {
      input.addEventListener('focus', () => {
        hint.style.display = 'inline';
      });
      input.addEventListener('blur', () => {
        hint.style.display = 'none';
      });
    }
  }
});
function formatFecha(dtStr){
  return dtStr;
}
