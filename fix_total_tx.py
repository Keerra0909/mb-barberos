import time, re

c = open('app.js', 'r', encoding='utf-8').read()

old_logic = """    const tbodyTx = document.getElementById('tabla-historial-tickets');
    if(tbodyTx) {
        tbodyTx.innerHTML = '';
        if(regsPeriodo.length === 0) {
            tbodyTx.innerHTML = '<tr><td colspan="6" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin registros en el periodo</td></tr>';
        }
        [...regsPeriodo].sort((a,b) => b.fechaObj - a.fechaObj).forEach(r => {
            const bPago = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
            const trClass = r.editado 
                ? 'border-l-2 border-l-orange-500 bg-orange-950/20 hover:bg-orange-950/30 transition-colors' 
                : 'hover:bg-zinc-900 transition-colors';
            const editBadge = r.editado 
                ? '<span class="ml-2 text-[8px] uppercase tracking-widest font-bold text-orange-400 bg-orange-900/30 border border-orange-700 px-1.5 py-0.5 rounded-sm">✎ Editado</span>' 
                : '';
            tbodyTx.innerHTML += `
                <tr class="${trClass}">
                    <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.fechaCorta}</td>
                    <td class="p-3 font-medium ${r.editado ? 'text-orange-300' : 'text-zinc-200'}">${r.barbero}</td>
                    <td class="p-3 text-zinc-300 text-xs">${r.servicio} ${editBadge}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                    <td class="p-3 text-zinc-500 font-mono text-xs">${formatoDinero.format(r.propina)}</td>
                    <td class="p-3 text-right pr-6"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${bPago}">${r.pagoTxt}</span></td>
                </tr>`;
        });
    }"""

new_logic = """    const tbodyTx = document.getElementById('tabla-historial-tickets');
    if(tbodyTx) {
        tbodyTx.innerHTML = '';
        if(regsPeriodo.length === 0) {
            tbodyTx.innerHTML = '<tr><td colspan="6" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin registros en el periodo</td></tr>';
        }
        let totalTxMonto = 0;
        let totalTxPropina = 0;
        [...regsPeriodo].sort((a,b) => b.fechaObj - a.fechaObj).forEach(r => {
            totalTxMonto += r.monto;
            totalTxPropina += r.propina;
            const bPago = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
            const trClass = r.editado 
                ? 'border-l-2 border-l-orange-500 bg-orange-950/20 hover:bg-orange-950/30 transition-colors' 
                : 'hover:bg-zinc-900 transition-colors';
            const editBadge = r.editado 
                ? '<span class="ml-2 text-[8px] uppercase tracking-widest font-bold text-orange-400 bg-orange-900/30 border border-orange-700 px-1.5 py-0.5 rounded-sm">✎ Editado</span>' 
                : '';
            tbodyTx.innerHTML += `
                <tr class="${trClass}">
                    <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.fechaCorta}</td>
                    <td class="p-3 font-medium ${r.editado ? 'text-orange-300' : 'text-zinc-200'}">${r.barbero}</td>
                    <td class="p-3 text-zinc-300 text-xs">${r.servicio} ${editBadge}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                    <td class="p-3 text-zinc-500 font-mono text-xs">${formatoDinero.format(r.propina)}</td>
                    <td class="p-3 text-right pr-6"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${bPago}">${r.pagoTxt}</span></td>
                </tr>`;
        });
        if (totalTxMonto > 0 || totalTxPropina > 0) {
            tbodyTx.innerHTML += `
                <tr class="bg-zinc-900/80 font-bold border-t border-zinc-700">
                    <td class="p-3 text-right pr-6 text-zinc-300 uppercase tracking-widest text-xs" colspan="3">TOTAL TICKETS</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(totalTxMonto)}</td>
                    <td class="p-3 text-zinc-400 font-mono tracking-wider text-xs">${formatoDinero.format(totalTxPropina)}</td>
                    <td class="p-3"></td>
                </tr>`;
        }
    }"""

c = c.replace(old_logic, new_logic)
open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Added total row to tickets history.")
