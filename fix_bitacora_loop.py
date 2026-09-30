import time, re

c = open('app.js', 'r', encoding='utf-8').read()

old_loop = """    regsHoy.forEach(r => {
        totalIngresos += r.monto; cEf += r.valEfectivo; cTar += r.valTarjeta;
        let b = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
        const badgeEdit = r.editado ? `<span class="ml-2 text-[9px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 rounded-sm">Editado</span>` : '';
        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-3 text-zinc-400 font-sans text-[11px] uppercase tracking-widest pl-6">${r.sucursal}</td>
                <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
                <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>
                <td class="p-3 text-zinc-300">${r.servicio} ${badgeEdit}</td>
                <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.propina)}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${b}">${r.pagoTxt}</span></td>
                <td class="p-3 pr-6 text-right">
                    <button onclick="abrirModalEditar(${r.id})" class="text-zinc-500 hover:text-white transition-colors" title="Editar"><i class="fa-solid fa-pen text-[11px]"></i></button>
                </td>
            </tr>`;
    });"""

new_loop = """    let cEfBruto = 0;
    let totalGastos = 0;
    regsHoy.forEach(r => {
        if(r.tipo === 'Gasto') {
            totalGastos += r.monto;
            tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors bg-red-950/10 border-l-2 border-red-500">
                <td class="p-3 text-zinc-400 font-sans text-[11px] uppercase tracking-widest pl-6">${r.sucursal}</td>
                <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
                <td class="p-3 font-medium text-red-400">-</td>
                <td class="p-3 text-red-400 font-bold text-xs uppercase tracking-widest">Gasto: ${r.servicio}</td>
                <td class="p-3 text-red-500 font-mono tracking-wider">- ${formatoDinero.format(r.monto)}</td>
                <td class="p-3 text-zinc-600">-</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Caja</span></td>
                <td class="p-3 pr-6"></td>
            </tr>`;
        } else {
            totalIngresos += r.monto; cEfBruto += r.valEfectivo; cTar += r.valTarjeta;
            let b = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
            const badgeEdit = r.editado ? `<span class="ml-2 text-[9px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 rounded-sm">Editado</span>` : '';
            tbody.innerHTML += `
                <tr class="hover:bg-zinc-900 transition-colors">
                    <td class="p-3 text-zinc-400 font-sans text-[11px] uppercase tracking-widest pl-6">${r.sucursal}</td>
                    <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
                    <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>
                    <td class="p-3 text-zinc-300 text-xs">${r.servicio} ${badgeEdit}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider text-xs">${formatoDinero.format(r.propina)}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${b}">${r.pagoTxt}</span></td>
                    <td class="p-3 pr-6 text-right">
                        <button onclick="abrirModalEditar(${r.id})" class="text-zinc-500 hover:text-white transition-colors" title="Editar"><i class="fa-solid fa-pen text-[11px]"></i></button>
                    </td>
                </tr>`;
        }
    });
    cEf = cEfBruto - totalGastos;
    // Asignar variables globales para el modal
    window.cajaEfectivoActual = cEf;
    window.gastosTotalesActuales = totalGastos;
    window.ingresosEfvoActuales = cEfBruto;"""

c = c.replace(old_loop, new_loop)
open('app.js', 'w', encoding='utf-8').write(c)

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Bitacora loop updated properly!")
