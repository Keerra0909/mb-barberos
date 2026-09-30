import time, re

c = open('app.js', 'r', encoding='utf-8').read()

pattern = re.compile(r'function renderizarListaModal\(contenedorId, arrayOriginal, fnEliminar\) \{.*?\}(?=\s*function|\s*window|\s*const|\s*$)', re.DOTALL)

new_render = """function renderizarListaModal(contenedorId, arrayOriginal, fnEliminar) {
    const container = document.getElementById(contenedorId); 
    if(!container) return;
    container.innerHTML = '';
    if(arrayOriginal.length === 0) { container.innerHTML = '<div class="p-4 text-xs text-zinc-600 text-center uppercase tracking-widest">Vacío</div>'; return; }
    
    let items = [...arrayOriginal];
    if(items.length > 0 && typeof items[0] === 'object') {
        items.sort((a,b)=>a.nombre.localeCompare(b.nombre));
    } else {
        items.sort();
    }
    
    items.forEach(item => {
        let isObj = typeof item === 'object';
        let val = isObj ? item.nombre : item;
        let sub = isObj ? item.sucursal : '';
        
        let pr = '';
        if (contenedorId === 'lista-servicios-modal' || contenedorId === 'lista-productos-modal') {
            pr = `<div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[val]}" onchange="actualizarPrecioServicio('${val}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div>`;
        } else if (sub) {
            pr = `<span class="text-[10px] text-zinc-500 tracking-widest uppercase">${sub}</span>`;
        }
        
        container.innerHTML += `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${val}</span>${pr}</div><button type="button" onclick="${fnEliminar}('${val}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`;
    });
}"""

c = re.sub(pattern, new_render + '\n', c)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("renderizarListaModal fixed via regex.")
