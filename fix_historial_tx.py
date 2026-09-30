c = open('app.js', 'r', encoding='utf-8').read()

old_row = """        [...regsPeriodo].sort((a,b) => b.fechaObj - a.fechaObj).forEach(r => {
            const bPago = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
            const editBadge = r.editado ? '<span class="ml-1 text-[8px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 py-0.5 rounded-sm">Editado</span>' : '';
            tbodyTx.innerHTML += `
                <tr class="hover:bg-zinc-900 transition-colors">
                    <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.fechaCorta}</td>
                    <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>
                    <td class="p-3 text-zinc-300 text-xs">${r.servicio} ${editBadge}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                    <td class="p-3 text-zinc-500 font-mono text-xs">${formatoDinero.format(r.propina)}</td>
                    <td class="p-3 text-right pr-6"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${bPago}">${r.pagoTxt}</span></td>
                </tr>`;
        });"""

new_row = """        [...regsPeriodo].sort((a,b) => b.fechaObj - a.fechaObj).forEach(r => {
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
        });"""

c = c.replace(old_row, new_row, 1)
open('app.js', 'w', encoding='utf-8').write(c)
print('done')
