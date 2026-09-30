import time, re

c = open('app.js', 'r', encoding='utf-8').read()

old_logic = """    barberosLocal.sort().forEach(b => {
        const s = stats[b];
        grid.innerHTML += `
            <div class="bg-zinc-900 border border-zinc-800 p-4 rounded-sm flex flex-col items-center justify-center">
                <span class="font-sans font-bold text-zinc-200 mb-1">${b}</span>
                <span class="text-[10px] uppercase tracking-widest text-zinc-500">${s.cortes} Tickets</span>
                <span class="text-emerald-400 font-mono tracking-wider mt-2">${formatoDinero.format(s.total)}</span>
            </div>
        `;
    });"""

new_logic = """    let renderedCount = 0;
    barberosLocal.sort().forEach(b => {
        const s = stats[b];
        if(s.cortes > 0) {
            renderedCount++;
            grid.innerHTML += `
                <div class="bg-zinc-900 border border-zinc-800 p-4 rounded-sm flex flex-col items-center justify-center">
                    <span class="font-sans font-bold text-zinc-200 mb-1">${b}</span>
                    <span class="text-[10px] uppercase tracking-widest text-zinc-500">${s.cortes} Tickets</span>
                    <span class="text-emerald-400 font-mono tracking-wider mt-2">${formatoDinero.format(s.total)}</span>
                </div>
            `;
        }
    });
    
    if (renderedCount === 0) {
        grid.innerHTML = '<div class="col-span-full text-xs text-zinc-600 text-center uppercase tracking-widest py-8">Aún no hay tickets generados hoy</div>';
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

print("Barber performance hidden if 0 tickets.")
