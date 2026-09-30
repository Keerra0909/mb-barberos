import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# 1. Add historialEdiciones array
js = js.replace("""let pagosNomina = JSON.parse(localStorage.getItem('mb_pagos')) || [];""", """let pagosNomina = JSON.parse(localStorage.getItem('mb_pagos')) || [];
let historialEdiciones = JSON.parse(localStorage.getItem('mb_ediciones')) || [];""")

js = js.replace("""localStorage.setItem('mb_pagos', JSON.stringify(pagosNomina));""", """localStorage.setItem('mb_pagos', JSON.stringify(pagosNomina));
    localStorage.setItem('mb_ediciones', JSON.stringify(historialEdiciones));""")

# 2. Update editBtn to be visible to all
old_editBtn = """const editBtn = rolActual === 'admin' ? `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-white transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>` : '';"""
new_editBtn = """const editBtn = `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-white transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>`;"""
js = js.replace(old_editBtn, new_editBtn)

old_gasto_btn = """<td class="p-3 text-right">${rolActual === 'admin' ? `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-red-400 transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>` : ''}</td>"""
new_gasto_btn = """<td class="p-3 text-right"><button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-red-400 transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button></td>"""
js = js.replace(old_gasto_btn, new_gasto_btn)

# 3. Log the edits in form-editar-ticket
old_submit_edit = """    const r = registros.find(x => x.id == id);
    if(r) {
        r.barbero = document.getElementById('edit-barbero').value;
        r.monto = parseFloat(document.getElementById('edit-monto').value) || 0;
        r.propina = parseFloat(document.getElementById('edit-propina').value) || 0;
        r.pagoTxt = document.getElementById('edit-pago').value;
        r.editado = true;
        guardarDatos();
        actualizarVistaHoy();
        actualizarReportes();
    }
    cerrarModalEditar();
});"""

new_submit_edit = """    const r = registros.find(x => x.id == id);
    if(r) {
        let oldStr = `${r.barbero} | Monto: $${r.monto} | Propina: $${r.propina} | Pago: ${r.pagoTxt}`;
        r.barbero = document.getElementById('edit-barbero').value;
        r.monto = parseFloat(document.getElementById('edit-monto').value) || 0;
        r.propina = parseFloat(document.getElementById('edit-propina').value) || 0;
        r.pagoTxt = document.getElementById('edit-pago').value;
        r.editado = true;
        let newStr = `${r.barbero} | Monto: $${r.monto} | Propina: $${r.propina} | Pago: ${r.pagoTxt}`;
        
        historialEdiciones.unshift({
            id: Date.now(),
            fecha: new Date().toLocaleString('es-MX', {day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit'}),
            ticketInfo: `[${r.sucursal}] ${r.fechaCorta} ${r.hora} - ${r.servicio || 'Gasto'}`,
            antes: oldStr,
            despues: newStr,
            usuario: rolActual === 'admin' ? 'Admin' : r.sucursal
        });
        
        guardarDatos();
        actualizarVistaHoy();
        actualizarReportes();
    }
    cerrarModalEditar();
});"""
js = js.replace(old_submit_edit, new_submit_edit)

# 4. In actualizarReportes, render the new table
old_rep = """    // Charts
    const isDark = true;"""

new_rep = """    // Tabla Ediciones
    const tbodyEdiciones = document.getElementById('tabla-historial-ediciones');
    if(tbodyEdiciones) {
        tbodyEdiciones.innerHTML = '';
        const edicsPeriodo = historialEdiciones.filter(e => {
            const fd = e.fecha.split(',')[0].split('/'); // DD/MM/YYYY
            const d = new Date(fd[2], fd[1]-1, fd[0]);
            return d >= inicio && d <= fin;
        });
        if(edicsPeriodo.length === 0) {
            tbodyEdiciones.innerHTML = `<tr><td colspan="4" class="p-6 text-center text-zinc-600">No hay modificaciones en este periodo.</td></tr>`;
        } else {
            edicsPeriodo.forEach(e => {
                tbodyEdiciones.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors">
                    <td class="p-3 text-zinc-500 whitespace-nowrap">${e.fecha}<br><span class="text-orange-400 text-[9px] uppercase">${e.usuario}</span></td>
                    <td class="p-3 text-zinc-300 font-bold">${e.ticketInfo}</td>
                    <td class="p-3 text-red-400 text-xs">${e.antes}</td>
                    <td class="p-3 text-emerald-400 text-xs">${e.despues}</td>
                </tr>`;
            });
        }
    }

    // Charts
    const isDark = true;"""
js = js.replace(old_rep, new_rep)

open('app.js', 'w', encoding='utf-8').write(js)

# 5. Add the table to index.html in the Reportes tab
html = open('index.html', 'r', encoding='utf-8').read()

new_table_html = """
                    <!-- Historial de Ediciones -->
                    <div class="glass-panel rounded-sm overflow-hidden mt-8 border border-orange-900/30">
                        <div class="p-4 border-b border-zinc-800 bg-black text-center">
                            <h2 class="text-xs font-sans font-bold text-orange-500 tracking-widest uppercase"><i class="fa-solid fa-triangle-exclamation mr-2"></i> Auditoría de Modificaciones</h2>
                        </div>
                        <div class="overflow-x-auto max-h-64">
                            <table class="w-full text-left text-[11px]">
                                <thead class="bg-[#050505] text-zinc-600 uppercase tracking-widest sticky top-0 border-b border-zinc-800">
                                    <tr>
                                        <th class="p-3 font-normal pl-6">Fecha Edición</th>
                                        <th class="p-3 font-normal">Ticket Afectado</th>
                                        <th class="p-3 font-normal">Antes</th>
                                        <th class="p-3 font-normal">Después</th>
                                    </tr>
                                </thead>
                                <tbody id="tabla-historial-ediciones" class="divide-y divide-zinc-900"></tbody>
                            </table>
                        </div>
                    </div>
"""

# Insert it after the Historial de Pagos table
html = html.replace("""                                  <tbody id="tabla-historial-pagos" class="divide-y divide-zinc-900"></tbody>
                              </table>
                          </div>
                          </div>""", """                                  <tbody id="tabla-historial-pagos" class="divide-y divide-zinc-900"></tbody>
                              </table>
                          </div>
                          </div>""" + new_table_html)

# Bust cache
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
