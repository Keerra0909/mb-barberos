import re, time

js = open('app.js', 'r', encoding='utf-8').read()

new_agregar = """window.agregarBebida = function() {
    const sel = document.getElementById('bebida');
    if(!sel || !sel.value || sel.value === '-' || sel.value === 'Sin cortesía') return;
    const s = sel.value;
    const tag = "🍹 " + s;
    if(!serviciosActuales.includes(tag)) {
        serviciosActuales.push(tag);
        actualizarUISeleccion();
    }
    sel.value = 'Sin cortesía';
};"""

js = js.replace("""window.agregarServicio = function() {""", new_agregar + "\n\nwindow.agregarServicio = function() {")

# Update registrar submit to also capture lingering bebida
old_submit = """    const valProd = document.getElementById('producto-item')?.value;
    if (valProd && !serviciosActuales.includes(valProd)) { serviciosActuales.push(valProd); }"""
new_submit = """    const valProd = document.getElementById('producto-item')?.value;
    if (valProd && !serviciosActuales.includes(valProd)) { serviciosActuales.push(valProd); }
    const valBeb = document.getElementById('bebida')?.value;
    if (valBeb && valBeb !== '-' && valBeb !== 'Sin cortesía' && !serviciosActuales.includes("🍹 " + valBeb)) { serviciosActuales.push("🍹 " + valBeb); }"""
js = js.replace(old_submit, new_submit)

# Update to not use r.bebida anymore in the row generation, since it's now in serviciosActuales
old_ticket = """        let strServicio = r.servicio + badgeEdit;
        if(r.bebida && r.bebida !== '-') strServicio += `<div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-1">🍹 Cortesía: ${r.bebida}</div>`;"""
new_ticket = """        let strServicio = (r.servicio || 'Servicio') + badgeEdit;
        if(r.bebida && r.bebida !== '-' && r.bebida !== 'Sin cortesía') {
            // Only add legacy bebida if it's not already in the servicio string
            if(!strServicio.includes(r.bebida)) {
                strServicio += `<div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-1">🍹 Cortesía: ${r.bebida}</div>`;
            }
        }"""
js = js.replace(old_ticket, new_ticket)

# Update the register save to just set bebida to '-' since it's now in tags
old_save = """const bebida = document.getElementById('bebida')?.value || '-';"""
new_save = """const bebida = '-';"""
js = js.replace(old_save, new_save)

open('app.js', 'w', encoding='utf-8').write(js)

# Update HTML to remove + button and add onchange to bebida
html = open('index.html', 'r', encoding='utf-8').read()

old_prod_html = """                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300" onchange="agregarProducto()">
                                            <option value="">+ Añadir Producto</option>
                                        </select>
                                        <button type="button" onclick="agregarProducto()" class="bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-300 px-3 rounded-sm text-xs transition-colors"><i class="fa-solid fa-plus"></i></button>
                                    </div>"""
new_prod_html = """                                    <select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300" onchange="agregarProducto()">
                                        <option value="">+ Añadir Producto</option>
                                    </select>"""
html = html.replace(old_prod_html, new_prod_html)

old_bebida_html = """<select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>"""
new_bebida_html = """<select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm" onchange="agregarBebida()"></select>"""
html = html.replace(old_bebida_html, new_bebida_html)

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
