import re, time

js = open('app.js', 'r', encoding='utf-8').read()

old_agregar = """window.agregarServicio = function() {
    const sel = document.getElementById('servicio');
    if(!sel || !sel.value) return;
    const s = sel.value;
    if(!serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        // Auto-update monto
        const montoEl = document.getElementById('monto');
        if(montoEl) montoEl.value = (parseFloat(montoEl.value) || 0) + (preciosBase[s] || 0);
        actualizarUISeleccion();
        calcularRestanteMixto();
    }
};"""

new_agregar = """window.agregarServicio = function() {
    const sel = document.getElementById('servicio');
    if(!sel || !sel.value) return;
    const s = sel.value;
    if(!serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        // Auto-update monto
        const montoEl = document.getElementById('monto');
        if(montoEl) montoEl.value = (parseFloat(montoEl.value) || 0) + (preciosBase[s] || 0);
        actualizarUISeleccion();
        calcularRestanteMixto();
    }
    sel.value = '';
};"""

js = js.replace(old_agregar, new_agregar)

# Also update the submit form to avoid double counting if something is lingering in the dropdowns
old_submit = """const servicioStr = serviciosActuales.join(' + ') || document.getElementById('servicio')?.value || 'Servicio';"""
new_submit = """
    // Si dejaron algo seleccionado pero no le dieron +, lo sumamos
    const valServ = document.getElementById('servicio')?.value;
    if (valServ && !serviciosActuales.includes(valServ)) { serviciosActuales.push(valServ); }
    const valProd = document.getElementById('producto-item')?.value;
    if (valProd && !serviciosActuales.includes(valProd)) { serviciosActuales.push(valProd); }

    const servicioStr = serviciosActuales.join(' + ') || 'Servicio';"""
js = js.replace(old_submit, new_submit)
open('app.js', 'w', encoding='utf-8').write(js)

# Update index.html to add onchange to the select
html = open('index.html', 'r', encoding='utf-8').read()
html = html.replace("""<select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>""", """<select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm" onchange="agregarServicio()"></select>""")
html = html.replace("""<select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">""", """<select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300" onchange="agregarProducto()">""")

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
