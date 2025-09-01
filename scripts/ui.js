
// Simple helpers for rendering and navigation
function $(sel, ctx=document){ return ctx.querySelector(sel); }
function $all(sel, ctx=document){ return Array.from(ctx.querySelectorAll(sel)); }
function go(url){ window.location.href = url; }
function formatFecha(dtStr){
  return dtStr;
}
