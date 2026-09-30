import time, re

c = open('index.html', 'r', encoding='utf-8', errors='ignore').read()

# Replace NA3mina encoding bug if present
c = c.replace('NA3mina', 'Nómina')
c = c.replace('AcciA3n', 'Acción')

old_nomina_th = """                                    <tr>
                                        <th class="p-4 font-normal text-left">Barbero</th>
                                        <th class="p-4 font-normal">Generado</th>
                                        <th class="p-4 font-normal">Abonado</th>
                                        <th class="p-4 font-normal text-right">Saldo</th>
                                        <th class="p-4 font-normal">Acción</th>
                                    </tr>"""

new_nomina_th = """                                    <tr>
                                        <th class="p-4 font-normal text-left">Barbero</th>
                                        <th class="p-4 font-normal text-zinc-500" title="Ventas Totales">Ventas Brutas</th>
                                        <th class="p-4 font-normal text-emerald-500 font-bold" title="50% Servicio + Propina">Sueldo / Comisión</th>
                                        <th class="p-4 font-normal text-blue-500">Pagado</th>
                                        <th class="p-4 font-normal text-right text-red-500">Saldo a Pagar</th>
                                        <th class="p-4 font-normal">Acción</th>
                                    </tr>"""

c = c.replace(old_nomina_th, new_nomina_th)
open('index.html', 'w', encoding='utf-8').write(c)


js = open('app.js', 'r', encoding='utf-8').read()

old_nomina_logic = """    const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { generado: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        const ganancia = (r.monto * 0.5) + r.propina;
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        if(mapNomina[r.barbero]) mapNomina[r.barbero].generado += ganancia;
    });

    pagosPeriodo.forEach(p => {
        if(mapNomina[p.barbero]) mapNomina[p.barbero].pagado += p.monto;
    });
    
    const tbodyNomina = document.getElementById('tabla-nomina-barberos'); tbodyNomina.innerHTML = '';
    if(Object.keys(mapNomina).length === 0) tbodyNomina.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin datos en periodo</td></tr>`;
    
    let totGenerado = 0, totPagado = 0, totSaldo = 0;
    
    Object.keys(mapNomina).sort().forEach(b => {
        const stats = mapNomina[b];
        const saldo = stats.generado - stats.pagado;
        if(stats.generado === 0 && stats.pagado === 0) return;
        totGenerado += stats.generado; totPagado += stats.pagado; totSaldo += saldo;
        
        tbodyNomina.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-4 font-medium text-left text-zinc-200">${b}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-400 font-mono tracking-wider">${formatoDinero.format(stats.generado)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-400 font-mono tracking-wider">${formatoDinero.format(stats.pagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-400 font-mono tracking-wider font-bold">${formatoDinero.format(saldo)}</td>
                <td class="p-4 text-center">
                    <button onclick="abrirModalLiquidacion('${b}', ${saldo})" class="bg-emerald-950 text-emerald-500 border border-emerald-900 hover:bg-emerald-900 hover:text-emerald-100 px-3 py-1 rounded-sm text-[10px] tracking-widest uppercase transition-colors">Liquidar</button>
                </td>
            </tr>`;
    });
    
    if(totGenerado > 0 || totPagado > 0) {
        tbodyNomina.innerHTML += `
            <tr class="bg-zinc-950 border-t border-zinc-800 font-bold">
                <td class="p-4 text-left text-zinc-300 text-[10px] tracking-widest uppercase">Totales</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-300 font-mono tracking-wider">${formatoDinero.format(totGenerado)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-300 font-mono tracking-wider">${formatoDinero.format(totPagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-500 font-mono tracking-wider">${formatoDinero.format(totSaldo)}</td>
                <td class="p-4"></td>
            </tr>`;
    }"""

new_nomina_logic = """    const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { ventasBrutas: 0, sueldo: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        // Sueldo = 50% of tickets + 100% of tips. (If they sell a product, right now it splits 50% too. Let's assume that's intended unless requested otherwise).
        const ganancia = (r.monto * 0.5) + r.propina;
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        if(mapNomina[r.barbero]) {
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
                <td class="p-4 text-center border-l border-zinc-900 text-emerald-400 font-mono tracking-wider font-bold bg-emerald-950/10">${formatoDinero.format(stats.sueldo)}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-400 font-mono tracking-wider">${formatoDinero.format(stats.pagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 text-red-400 font-mono tracking-wider font-bold">${formatoDinero.format(saldo)}</td>
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
js = js.replace(old_nomina_logic, new_nomina_logic)

open('app.js', 'w', encoding='utf-8').write(js)

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Nomina updated to show Ventas Brutas and Sueldo/Comision clearly")
