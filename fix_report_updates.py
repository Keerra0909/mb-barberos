import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Fix 1: Make sucursal-select update the reports if visible
js = js.replace("""const selSuc = document.getElementById('sucursal-select');
if(selSuc) selSuc.addEventListener('change', e => {
    sucursalActual = e.target.value;
    const lbl = document.getElementById('label-sucursal-form');
    if(lbl) lbl.textContent = sucursalActual;
    actualizarVistaHoy();
    actualizarSelectsForm();
});""", """const selSuc = document.getElementById('sucursal-select');
if(selSuc) selSuc.addEventListener('change', e => {
    sucursalActual = e.target.value;
    const lbl = document.getElementById('label-sucursal-form');
    if(lbl) lbl.textContent = sucursalActual;
    actualizarVistaHoy();
    actualizarSelectsForm();
    const vistaRep = document.getElementById('vista-reportes');
    if(vistaRep && !vistaRep.classList.contains('hidden')) {
        actualizarReportes();
    }
});""")

# Fix 2: Add total row to Historial de Pagos table
# We look for the loop that fills tbodyPagos
old_pagos_loop = """        [...pagosPeriodo].sort((a,b) => b.fechaObj-a.fechaObj).forEach(p => {
            tbodyPagos.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors"><td class="p-3 text-zinc-500">${p.fechaStr}</td><td class="p-3 font-bold text-zinc-200">${p.barbero}</td><td class="p-3 text-emerald-400 font-mono font-bold">${formatoDinero.format(p.monto)}</td><td class="p-3 text-zinc-400">${p.metodo}</td></tr>`;
        });"""

new_pagos_loop = """        let totalPagadoHistorial = 0;
        [...pagosPeriodo].sort((a,b) => b.fechaObj-a.fechaObj).forEach(p => {
            totalPagadoHistorial += p.monto;
            tbodyPagos.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors"><td class="p-3 text-zinc-500">${p.fechaStr}</td><td class="p-3 font-bold text-zinc-200">${p.barbero}</td><td class="p-3 text-emerald-400 font-mono font-bold">${formatoDinero.format(p.monto)}</td><td class="p-3 text-zinc-400">${p.metodo}</td></tr>`;
        });
        if(pagosPeriodo.length > 0) {
            tbodyPagos.innerHTML += `<tr class="bg-zinc-950 border-t border-zinc-800 font-bold"><td colspan="2" class="p-3 text-right text-zinc-300 text-[10px] tracking-widest uppercase">Total Pagado:</td><td class="p-3 text-emerald-400 font-mono font-bold text-left">${formatoDinero.format(totalPagadoHistorial)}</td><td></td></tr>`;
        }"""

js = js.replace(old_pagos_loop, new_pagos_loop)
open('app.js', 'w', encoding='utf-8').write(js)

# Fix 3: Change title in index.html
html = open('index.html', 'r', encoding='utf-8').read()
html = html.replace("""<h2 class="text-xs font-sans font-bold text-zinc-400 tracking-widest uppercase">Historial de Tickets</h2>""", """<h2 class="text-xs font-sans font-bold text-zinc-400 tracking-widest uppercase">Historial de Pagos Emitidos</h2>""")

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
