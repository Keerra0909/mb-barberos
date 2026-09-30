c = open('app.js', 'r', encoding='utf-8').read()

old_row = """        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.hora}</td>
                <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>"""

new_row = """        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-3 text-zinc-400 font-sans text-[11px] uppercase tracking-widest pl-6">${r.sucursal}</td>
                <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
                <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>"""

c = c.replace(old_row, new_row, 1)

# Also fix the "colspan" from 7 to 8 for "Sin registros"
c = c.replace('colspan="7"', 'colspan="8"')

open('app.js', 'w', encoding='utf-8').write(c)

# We need to bump cache again so user gets the change!
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = sw.replace("CACHE_NAME = 'mb-barberos-v2'", "CACHE_NAME = 'mb-barberos-v3'")
open('sw.js', 'w', encoding='utf-8').write(sw)

import time
idx = open('index.html', 'r', encoding='utf-8').read()
import re
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

print("Local column added and cache bumped!")
