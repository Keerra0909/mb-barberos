import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Make toggleMixto and calcularRestanteMixto explicitly global
js = js.replace("""function toggleMixto(isMixto) {""", """window.toggleMixto = function(isMixto) {""")
js = js.replace("""function calcularRestanteMixto() {""", """window.calcularRestanteMixto = function() {""")

# Add edit functions
new_edit_funcs = """window.toggleMixtoEdit = function() {
    const pagoSel = document.getElementById('edit-pago');
    const p = document.getElementById('edit-panel-mixto');
    if(p && pagoSel) {
        if(pagoSel.value === 'Mixto') {
            p.classList.remove('hidden');
            window.calcularRestanteMixtoEdit();
        } else {
            p.classList.add('hidden');
        }
    }
};

window.calcularRestanteMixtoEdit = function() {
    const p = document.getElementById('edit-panel-mixto');
    if(!p || p.classList.contains('hidden')) return;
    const m = parseFloat(document.getElementById('edit-monto')?.value) || 0;
    const pr = parseFloat(document.getElementById('edit-propina')?.value) || 0;
    const total = m + pr;
    const lbl = document.getElementById('edit-total-mixto-label');
    if(lbl) lbl.textContent = formatoDinero.format(total);
    
    const ef = parseFloat(document.getElementById('edit-monto-efectivo-mixto')?.value) || 0;
    const rest = Math.max(0, total - ef);
    const rlbl = document.getElementById('edit-restante-tarjeta-label');
    if(rlbl) rlbl.textContent = formatoDinero.format(rest);
};"""

js = js.replace("""window.cerrarModalEditar = function() { ticketEnEdicion = null; if(modalEditar) modalEditar.classList.add('hidden'); };""", """window.cerrarModalEditar = function() { ticketEnEdicion = null; if(modalEditar) modalEditar.classList.add('hidden'); };\n\n""" + new_edit_funcs)

# Update the edit modal open to bind event
old_abrir = """const epago = document.getElementById('edit-pago'); if(epago) epago.value = reg.pagoTxt;"""
new_abrir = """const epago = document.getElementById('edit-pago'); if(epago) { epago.value = reg.pagoTxt; epago.addEventListener('change', window.toggleMixtoEdit); window.toggleMixtoEdit(); }"""
js = js.replace(old_abrir, new_abrir)

open('app.js', 'w', encoding='utf-8').write(js)

# HTML changes for Edit modal
html = open('index.html', 'r', encoding='utf-8').read()
html = html.replace("""<select id="edit-pago" class="w-full input-dark rounded-sm p-3 text-sm text-center font-bold">""", """<select id="edit-pago" class="w-full input-dark rounded-sm p-3 text-sm text-center font-bold" onchange="toggleMixtoEdit()">""")

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
