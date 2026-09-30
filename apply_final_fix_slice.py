import time, re

js = open('app.js', 'r', encoding='utf-8').read()

# Replace the whole mapNomina calculation logic down to the end of the table drawing loop
# Find start
start_idx = js.find('const mapNomina = {};')
# Find end
end_idx = js.find('</tr>`;\n    }') + len('</tr>`;\n    }')

if start_idx != -1 and end_idx != -1:
    old_code = js[start_idx:end_idx]
    new_code = """const mapNomina = {};
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
                <td class="p-4 text-center border-l border-zinc-900 text-emerald-500 font-mono tracking-wider">
                    <div class="flex flex-col items-center">
                        <span>${formatoDinero.format(totSueldo)}</span>
                        <span class="text-[10px] text-zinc-500">+${formatoDinero.format(totProps)}</span>
                    </div>
                </td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-500 font-mono tracking-wider">${formatoDinero.format(totPagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-500 font-mono tracking-wider">${formatoDinero.format(totSaldo)}</td>
                <td class="p-4"></td>
            </tr>`;
    }"""
    js = js.replace(old_code, new_code)
    open('app.js', 'w', encoding='utf-8').write(js)
    print("SUCCESS")
else:
    print("FAILED")

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
