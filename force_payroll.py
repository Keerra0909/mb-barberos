import time, re

c = open('app.js', 'r', encoding='utf-8').read()

pattern = re.compile(r'(const mapNomina = \{\};\s*barberosLocal\.forEach\(b => mapNomina\[b\] = \{.*?\};\s*\}\);)', re.DOTALL)

def replacer(match):
    return """const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { ventasBrutas: 0, sueldo: 0, pagado: 0 });

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

c = re.sub(pattern, replacer, c)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Payroll regex forced.")
