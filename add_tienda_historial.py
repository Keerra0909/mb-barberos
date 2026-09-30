import time, re

# Update HTML
c = open('index.html', 'r', encoding='utf-8').read()

old_thead = """                                    <tr>
                                        <th class="p-3 font-normal text-left pl-6">Fecha</th>
                                        <th class="p-3 font-normal">Barbero</th>"""

new_thead = """                                    <tr>
                                        <th class="p-3 font-normal text-left pl-6">Local</th>
                                        <th class="p-3 font-normal text-left">Fecha</th>
                                        <th class="p-3 font-normal">Barbero</th>"""
c = c.replace(old_thead, new_thead)
open('index.html', 'w', encoding='utf-8').write(c)


# Update app.js
js = open('app.js', 'r', encoding='utf-8').read()

old_row = """            tbodyTx.innerHTML += `
                <tr class="${trClass}">
                    <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.fechaCorta}</td>
                    <td class="p-3 font-medium ${r.editado ? 'text-orange-300' : 'text-zinc-200'}">${r.barbero}</td>"""

new_row = """            tbodyTx.innerHTML += `
                <tr class="${trClass}">
                    <td class="p-3 text-zinc-400 font-sans text-[11px] uppercase tracking-widest pl-6">${r.sucursal}</td>
                    <td class="p-3 text-zinc-500 font-mono text-xs">${r.fechaCorta}</td>
                    <td class="p-3 font-medium ${r.editado ? 'text-orange-300' : 'text-zinc-200'}">${r.barbero}</td>"""
js = js.replace(old_row, new_row)

old_colspan_total = '<td class="p-3 text-right pr-6 text-zinc-300 uppercase tracking-widest text-xs" colspan="3">TOTAL TICKETS</td>'
new_colspan_total = '<td class="p-3 text-right pr-6 text-zinc-300 uppercase tracking-widest text-xs" colspan="4">TOTAL TICKETS</td>'
js = js.replace(old_colspan_total, new_colspan_total)

old_colspan_empty = '<td colspan="6" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin registros en el periodo</td>'
new_colspan_empty = '<td colspan="7" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">Sin registros en el periodo</td>'
js = js.replace(old_colspan_empty, new_colspan_empty)

open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Local column added to historical tickets.")
