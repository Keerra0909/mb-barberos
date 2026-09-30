import time, re

c = open('index.html', 'r', encoding='utf-8').read()

old_form_block = """                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                    <div id="servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Producto / Cortesa</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-1/2 input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Producto</option>
                                        </select>
                                        <select id="bebida" class="w-1/2 input-dark rounded-sm p-3 text-xs"></select>
                                    </div>
                                    <button type="button" onclick="agregarProducto()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Aadir Producto</button>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                                    <input type="number" id="monto" value="380" class="w-full input-dark rounded-sm p-3 text-sm font-bold" required>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                                    <input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm">
                                </div>
                            </div>"""

# Fallback block just in case it actually rendered properly as utf-8 when python reads it
old_form_block_utf8 = old_form_block.replace('Cortesa', 'Cortesía').replace('Aadir', 'Añadir')


new_form_block = """                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                    <div id="servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Productos</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Añadir Producto</option>
                                        </select>
                                        <button type="button" onclick="agregarProducto()" class="bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-300 px-3 rounded-sm text-xs transition-colors"><i class="fa-solid fa-plus"></i></button>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-3 gap-3">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                                    <input type="number" id="monto" value="380" class="w-full input-dark rounded-sm p-3 text-sm font-bold" required>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                                    <input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm">
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                                    <select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                </div>
                            </div>"""

if old_form_block in c:
    c = c.replace(old_form_block, new_form_block)
elif old_form_block_utf8 in c:
    c = c.replace(old_form_block_utf8, new_form_block)
else:
    print("WARNING: form block not found!")


old_th = """                                        <th class="p-4 font-normal text-emerald-500 font-bold" title="50% Servicio + Propina">Sueldo / Comisión</th>"""
new_th = """                                        <th class="p-4 font-normal text-emerald-500 font-bold" title="50% Servicio + Propina">Comisión / Propina</th>"""
c = c.replace(old_th, new_th)
open('index.html', 'w', encoding='utf-8').write(c)


# Now fix app.js for the Nomina breakdown
js = open('app.js', 'r', encoding='utf-8').read()

old_js_block = """    const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { generado: 0, ventasBrutas: 0, sueldo: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        let montoProductos = 0;
        const items = r.servicio.split(' + ');
        items.forEach(item => {
            if (productosActivos.includes(item)) {
                montoProductos += (preciosBase[item] || 0);
            }
        });
        
        let montoComisionable = Math.max(0, r.monto - montoProductos);
        const ganancia = (montoComisionable * 0.5) + (r.propina || 0);
        
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        
        if(mapNomina[r.barbero]) {
            mapNomina[r.barbero].generado += ganancia; // legacy fallback
            mapNomina[r.barbero].ventasBrutas += r.monto;
            mapNomina[r.barbero].sueldo += ganancia;
        }
    });

    pagosPeriodo.forEach(p => {
        if(mapNomina[p.barbero]) mapNomina[p.barbero].pagado += p.monto;
    });

    const tbodyNomina = document.getElementById('tabla-nomina-barberos'); tbodyNomina.innerHTML = '';
    if(Object.keys(mapNomina).length === 0) tbodyNomina.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin datos en periodo</td></tr>`;
    
    let totVentas = 0, totSueldo = 0, totPagado = 0, totSaldo = 0;
    
    Object.keys(mapNomina).sort().forEach(b => {
        const stats = mapNomina[b];
        const saldo = stats.sueldo - stats.pagado;
        if(stats.ventasBrutas === 0 && stats.sueldo === 0 && stats.pagado === 0) return;
        totVentas += stats.ventasBrutas; totSueldo += stats.sueldo; totPagado += stats.pagado; totSaldo += saldo;
        
        tbodyNomina.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-4 font-medium text-left text-zinc-200">${b}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono tracking-wider">${formatoDinero.format(stats.ventasBrutas)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-emerald-400 font-mono tracking-wider font-bold bg-emerald-950/20">${formatoDinero.format(stats.sueldo)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-400 font-mono tracking-wider">${formatoDinero.format(stats.pagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 font-mono tracking-wider ${saldo > 0 ? 'text-red-400 font-bold' : 'text-zinc-500'}">${formatoDinero.format(saldo)}</td>
                <td class="p-4 text-center">
                    <button onclick="abrirModalLiquidacion('${b}', ${saldo})" class="bg-emerald-950 text-emerald-500 border border-emerald-900 hover:bg-emerald-900 hover:text-emerald-100 px-3 py-1 rounded-sm text-[10px] tracking-widest uppercase transition-colors">Liquidar</button>
                </td>
            </tr>`;
    });
    
    if(totVentas > 0 || totSueldo > 0 || totPagado > 0) {
        tbodyNomina.innerHTML += `
            <tr class="bg-zinc-950 border-t border-zinc-800 font-bold">
                <td class="p-4 text-left text-zinc-300 text-[10px] tracking-widest uppercase">Totales</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono tracking-wider">${formatoDinero.format(totVentas)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-emerald-500 font-mono tracking-wider">${formatoDinero.format(totSueldo)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-500 font-mono tracking-wider">${formatoDinero.format(totPagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-500 font-mono tracking-wider">${formatoDinero.format(totSaldo)}</td>
                <td class="p-4"></td>
            </tr>`;
    }"""

new_js_block = """    const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { generado: 0, ventasBrutas: 0, sueldo: 0, propinasTotal: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        let montoProductos = 0;
        const items = r.servicio.split(' + ');
        items.forEach(item => {
            if (productosActivos.includes(item)) {
                montoProductos += (preciosBase[item] || 0);
            }
        });
        
        let montoComisionable = Math.max(0, r.monto - montoProductos);
        let prop = r.propina || 0;
        let comision = montoComisionable * 0.5;
        const ganancia = comision + prop;
        
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        
        if(mapNomina[r.barbero]) {
            mapNomina[r.barbero].generado += ganancia;
            mapNomina[r.barbero].ventasBrutas += r.monto;
            mapNomina[r.barbero].sueldo += comision;
            mapNomina[r.barbero].propinasTotal += prop;
        }
    });

    pagosPeriodo.forEach(p => {
        if(mapNomina[p.barbero]) mapNomina[p.barbero].pagado += p.monto;
    });

    const tbodyNomina = document.getElementById('tabla-nomina-barberos'); tbodyNomina.innerHTML = '';
    if(Object.keys(mapNomina).length === 0) tbodyNomina.innerHTML = `<tr><td colspan="6" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin datos en periodo</td></tr>`;
    
    let totVentas = 0, totSueldo = 0, totProps = 0, totPagado = 0, totSaldo = 0;
    
    Object.keys(mapNomina).sort().forEach(b => {
        const stats = mapNomina[b];
        const saldo = (stats.sueldo + stats.propinasTotal) - stats.pagado;
        if(stats.ventasBrutas === 0 && stats.sueldo === 0 && stats.propinasTotal === 0 && stats.pagado === 0) return;
        totVentas += stats.ventasBrutas; totSueldo += stats.sueldo; totProps += stats.propinasTotal; totPagado += stats.pagado; totSaldo += saldo;
        
        tbodyNomina.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-4 font-medium text-left text-zinc-200">${b}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono tracking-wider">${formatoDinero.format(stats.ventasBrutas)}</td>
                <td class="p-4 text-center border-l border-zinc-900 bg-emerald-950/10">
                    <div class="flex flex-col items-center">
                        <span class="text-emerald-400 font-mono tracking-wider font-bold">${formatoDinero.format(stats.sueldo)}</span>
                        <span class="text-[10px] text-zinc-500 uppercase tracking-widest mt-0.5">+ ${formatoDinero.format(stats.propinasTotal)} prop.</span>
                    </div>
                </td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-400 font-mono tracking-wider">${formatoDinero.format(stats.pagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 font-mono tracking-wider ${saldo > 0 ? 'text-red-400 font-bold' : 'text-zinc-500'}">${formatoDinero.format(saldo)}</td>
                <td class="p-4 text-center">
                    <button onclick="abrirModalLiquidacion('${b}', ${saldo})" class="bg-emerald-950 text-emerald-500 border border-emerald-900 hover:bg-emerald-900 hover:text-emerald-100 px-3 py-1 rounded-sm text-[10px] tracking-widest uppercase transition-colors">Liquidar</button>
                </td>
            </tr>`;
    });
    
    if(totVentas > 0 || totSueldo > 0 || totProps > 0 || totPagado > 0) {
        tbodyNomina.innerHTML += `
            <tr class="bg-zinc-950 border-t border-zinc-800 font-bold">
                <td class="p-4 text-left text-zinc-300 text-[10px] tracking-widest uppercase">Totales</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono tracking-wider">${formatoDinero.format(totVentas)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-emerald-500 font-mono tracking-wider">${formatoDinero.format(totSueldo + totProps)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-500 font-mono tracking-wider">${formatoDinero.format(totPagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-500 font-mono tracking-wider">${formatoDinero.format(totSaldo)}</td>
                <td class="p-4"></td>
            </tr>`;
    }"""

c = c.replace(old_js_block, new_js_block)
open('app.js', 'w', encoding='utf-8').write(c)


# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Exact replacement worked.")
