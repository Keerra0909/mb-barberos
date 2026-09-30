import re, time

js = open('app.js', 'r', encoding='utf-8').read()

old_gasto = """    gastosHoy.forEach(r => {
        tbody.innerHTML += `<tr class="hover:bg-zinc-900/50 transition-colors bg-red-950/10">
            <td class="p-3 text-zinc-600 text-xs pl-4">${r.hora}</td>
            <td class="p-3 text-red-400 font-bold text-xs">-</td>
            <td colspan="2" class="p-3 text-red-400 text-xs uppercase tracking-wider">Gasto: ${r.servicio}</td>
            <td class="p-3 text-red-500 font-mono text-xs">- ${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-zinc-600 text-xs">-</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Gasto</span></td>
            <td class="p-3 text-right">${rolActual === 'admin' ? `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-red-400 transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>` : ''}</td>
        </tr>`;
    });"""

new_gasto = """    gastosHoy.forEach(r => {
        tbody.innerHTML += `<tr class="hover:bg-zinc-900/50 transition-colors bg-red-950/10">
            <td class="p-3 text-zinc-600 text-[9px] uppercase tracking-widest pl-4">${r.sucursal}</td>
            <td class="p-3 text-zinc-600 font-mono text-xs">${r.hora}</td>
            <td class="p-3 text-red-400 font-bold text-xs">—</td>
            <td class="p-3 text-red-400 text-xs uppercase tracking-wider">Gasto: ${r.servicio}</td>
            <td class="p-3 text-red-500 font-mono text-xs">- ${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-zinc-600 text-xs">—</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Gasto</span></td>
            <td class="p-3 text-right">${rolActual === 'admin' ? `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-red-400 transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>` : ''}</td>
        </tr>`;
    });"""
js = js.replace(old_gasto, new_gasto)


old_ticket = """        tbody.innerHTML += `<tr class="${rowClass}">
            <td class="p-3 text-zinc-500 font-mono text-xs pl-4">${r.hora}</td>
            <td class="p-3 font-medium text-zinc-200 text-sm">${r.barbero}</td>
            <td class="p-3 text-zinc-300 text-xs">${r.servicio}${badgeEdit}</td>
            <td class="p-3 text-zinc-400 text-xs">${r.bebida !== '-' ? r.bebida : '-'}</td>
            <td class="p-3 text-emerald-400 font-mono tracking-wider text-sm">${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-emerald-300 font-mono text-xs">${r.propina > 0 ? '+' + formatoDinero.format(r.propina) : '-'}</td>
            <td class="p-3">${bPago}</td>
            <td class="p-3 text-right">${editBtn}</td>
        </tr>`;"""

new_ticket = """        let strServicio = r.servicio + badgeEdit;
        if(r.bebida && r.bebida !== '-') strServicio += `<div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-1">🍹 Cortesía: ${r.bebida}</div>`;
        tbody.innerHTML += `<tr class="${rowClass}">
            <td class="p-3 text-zinc-400 text-[10px] uppercase tracking-widest pl-4 font-bold">${r.sucursal}</td>
            <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
            <td class="p-3 font-medium text-zinc-200 text-sm">${r.barbero}</td>
            <td class="p-3 text-zinc-300 text-xs">${strServicio}</td>
            <td class="p-3 text-emerald-400 font-mono tracking-wider text-sm">${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-emerald-300 font-mono text-xs">${r.propina > 0 ? '+' + formatoDinero.format(r.propina) : '—'}</td>
            <td class="p-3">${bPago}</td>
            <td class="p-3 text-right">${editBtn}</td>
        </tr>`;"""
js = js.replace(old_ticket, new_ticket)

open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
