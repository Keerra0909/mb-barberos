import time, re

c = open('app.js', 'r', encoding='utf-8').read()

# 1. Fix actualizarTodasLasListas
old_listas = """function actualizarTodasLasListas() {
    renderizarListaModal('lista-sucursales-modal', sucursalesActivas, 'eliminarSucursal');
    renderizarListaModal('lista-barberos-modal', barberosActivos, 'eliminarBarbero');
    renderizarListaModal('lista-servicios-modal', serviciosActivos, 'eliminarServicio');
    renderizarListaModal('lista-bebidas-modal', bebidasActivas, 'eliminarBebida');
    
    const nsuc = document.getElementById('nuevo-barbero-sucursal');
    if(nsuc) nsuc.innerHTML = sucursalesActivas.map(s => `<option value="${s}">${s}</option>`).join('');
    
    actualizarMenuSucursalesHeader(); actualizarSelectsForm();
}"""

new_listas = """function actualizarTodasLasListas() {
    renderizarListaModal('lista-productos-modal', productosActivos, 'eliminarProducto');
    renderizarListaModal('lista-barberos-modal', barberosActivos, 'eliminarBarbero');
    renderizarListaModal('lista-servicios-modal', serviciosActivos, 'eliminarServicio');
    renderizarListaModal('lista-bebidas-modal', bebidasActivas, 'eliminarBebida');
    
    const nsuc = document.getElementById('nuevo-barbero-sucursal');
    if(nsuc) nsuc.innerHTML = sucursalesActivas.map(s => `<option value="${s}">${s}</option>`).join('');
    
    actualizarMenuSucursalesHeader(); 
    actualizarSelectsForm();
}"""
c = c.replace(old_listas, new_listas)

# 2. Make renderizarListaModal display prices properly for products
old_render = """function renderizarListaModal(contenedorId, arrayOriginal, fnEliminar) {
    const container = document.getElementById(contenedorId); container.innerHTML = '';
    if(arrayOriginal.length === 0) { container.innerHTML = '<div class="p-4 text-xs text-zinc-600 text-center uppercase tracking-widest">Vacío</div>'; return; }
    
    let arr = arrayOriginal;
    if(contenedorId === 'lista-barberos-modal') arr = [...arrayOriginal].sort((a,b)=>a.nombre.localeCompare(b.nombre));
    else arr = [...arrayOriginal].sort();
    
    arr.forEach(item => {
        const val = typeof item === 'object' ? item.nombre : item;
        const sub = typeof item === 'object' ? item.sucursal : '';
        const isServ = contenedorId === 'lista-servicios-modal';
        const pr = isServ ? `<div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[val]}" onchange="actualizarPrecioServicio('${val}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div>` : (sub ? `<span class="text-[10px] text-zinc-500 tracking-widest uppercase">${sub}</span>` : '');
        container.innerHTML += `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${val}</span>${pr}</div><button type="button" onclick="${fnEliminar}('${val}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`;
    });
}"""

new_render = """function renderizarListaModal(contenedorId, arrayOriginal, fnEliminar) {
    const container = document.getElementById(contenedorId); 
    if(!container) return; // fail gracefully
    container.innerHTML = '';
    if(arrayOriginal.length === 0) { container.innerHTML = '<div class="p-4 text-xs text-zinc-600 text-center uppercase tracking-widest">Vacío</div>'; return; }
    
    let arr = arrayOriginal;
    if(contenedorId === 'lista-barberos-modal') arr = [...arrayOriginal].sort((a,b)=>a.nombre.localeCompare(b.nombre));
    else arr = [...arrayOriginal].sort();
    
    arr.forEach(item => {
        const val = typeof item === 'object' ? item.nombre : item;
        const sub = typeof item === 'object' ? item.sucursal : '';
        const isServOrProd = contenedorId === 'lista-servicios-modal' || contenedorId === 'lista-productos-modal';
        const pr = isServOrProd ? `<div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[val]}" onchange="actualizarPrecioServicio('${val}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div>` : (sub ? `<span class="text-[10px] text-zinc-500 tracking-widest uppercase">${sub}</span>` : '');
        container.innerHTML += `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${val}</span>${pr}</div><button type="button" onclick="${fnEliminar}('${val}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`;
    });
}"""
c = c.replace(old_render, new_render)

# 3. Add agregarProducto function and update select loading
old_selects = """    catalog.forEach(grupo => {
        optServicios += `<optgroup label="${grupo.cat}" class="bg-zinc-900 text-zinc-400 font-sans font-bold uppercase tracking-widest text-xs">`;
        grupo.items.forEach(s => {
            if(serviciosActivos.includes(s)) optServicios += `<option value="${s}" class="bg-black text-sm text-zinc-200 normal-case font-normal">${s} - $${preciosBase[s]}</option>`;
        });
        optServicios += `</optgroup>`;
    });
    
    if(sBarbero) sBarbero.innerHTML = optBarberos; if(eBarbero) eBarbero.innerHTML = optBarberos;
    if(sServicio) sServicio.innerHTML = optServicios; if(eServicio) eServicio.innerHTML = optServicios;
    if(sBebida) sBebida.innerHTML = optBebidas; if(eBebida) eBebida.innerHTML = optBebidas;
}"""

new_selects = """    catalog.forEach(grupo => {
        optServicios += `<optgroup label="${grupo.cat}" class="bg-zinc-900 text-zinc-400 font-sans font-bold uppercase tracking-widest text-xs">`;
        grupo.items.forEach(s => {
            if(serviciosActivos.includes(s)) optServicios += `<option value="${s}" class="bg-black text-sm text-zinc-200 normal-case font-normal">${s} - $${preciosBase[s]}</option>`;
        });
        optServicios += `</optgroup>`;
    });
    
    if(sBarbero) sBarbero.innerHTML = optBarberos; if(eBarbero) eBarbero.innerHTML = optBarberos;
    if(sServicio) sServicio.innerHTML = optServicios; if(eServicio) eServicio.innerHTML = optServicios;
    if(sBebida) sBebida.innerHTML = optBebidas; if(eBebida) eBebida.innerHTML = optBebidas;
    
    const selProd = document.getElementById('producto-item');
    if(selProd) selProd.innerHTML = '<option value="">+ Producto...</option>' + productosActivos.sort().map(x => `<option value="${x}">${x} - $${preciosBase[x]||0}</option>`).join('');
}

window.agregarProducto = function() {
    const sel = document.getElementById('producto-item');
    const s = sel.value;
    if(s && !serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        const currentTotal = parseFloat(document.getElementById('monto').value) || 0;
        document.getElementById('monto').value = currentTotal + (preciosBase[s] || 0);
        actualizarUISeleccion();
        calcularRestanteMixto();
    }
    sel.value = '';
}
"""
c = c.replace(old_selects, new_selects)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("JS error fixed, renderizarListaModal updated.")
