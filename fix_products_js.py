import time, re

c = open('app.js', 'r', encoding='utf-8').read()

# 1. Update actualizarTodasLasListas
old_listas = """function actualizarTodasLasListas() {
    const listSuc = document.getElementById('lista-sucursales-modal'); if(listSuc) listSuc.innerHTML = sucursalesActivas.map(s => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${s}</span><button type="button" onclick="eliminarSucursal('${s}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listBarb = document.getElementById('lista-barberos-modal'); if(listBarb) listBarb.innerHTML = barberosActivos.sort((a,b)=>a.nombre.localeCompare(b.nombre)).map(b => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${b.nombre}</span><span class="text-[10px] text-zinc-500 tracking-widest uppercase">${b.sucursal}</span></div><button type="button" onclick="eliminarBarbero('${b.nombre}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listServ = document.getElementById('lista-servicios-modal'); if(listServ) listServ.innerHTML = serviciosActivos.sort().map(s => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-[11px] text-zinc-300 tracking-widest uppercase font-bold">${s}</span><div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[s]}" onchange="actualizarPrecioServicio('${s}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div></div><button type="button" onclick="eliminarServicio('${s}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listBeb = document.getElementById('lista-bebidas-modal'); if(listBeb) listBeb.innerHTML = bebidasActivas.map(b => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><span class="text-[11px] text-zinc-300 tracking-widest uppercase font-bold">${b}</span><button type="button" onclick="eliminarBebida('${b}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const nsuc = document.getElementById('nuevo-barbero-sucursal');
    if(nsuc) nsuc.innerHTML = sucursalesActivas.map(s => `<option value="${s}">${s}</option>`).join('');
    
    actualizarMenuSucursalesHeader(); actualizarSelectsForm();
}"""

new_listas = """function actualizarTodasLasListas() {
    const listProd = document.getElementById('lista-productos-modal'); if(listProd) listProd.innerHTML = productosActivos.sort().map(s => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-[11px] text-zinc-300 tracking-widest uppercase font-bold">${s}</span><div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[s]}" onchange="actualizarPrecioServicio('${s}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div></div><button type="button" onclick="eliminarProducto('${s}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listBarb = document.getElementById('lista-barberos-modal'); if(listBarb) listBarb.innerHTML = barberosActivos.sort((a,b)=>a.nombre.localeCompare(b.nombre)).map(b => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${b.nombre}</span><span class="text-[10px] text-zinc-500 tracking-widest uppercase">${b.sucursal}</span></div><button type="button" onclick="eliminarBarbero('${b.nombre}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listServ = document.getElementById('lista-servicios-modal'); if(listServ) listServ.innerHTML = serviciosActivos.sort().map(s => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-[11px] text-zinc-300 tracking-widest uppercase font-bold">${s}</span><div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[s]}" onchange="actualizarPrecioServicio('${s}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div></div><button type="button" onclick="eliminarServicio('${s}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const listBeb = document.getElementById('lista-bebidas-modal'); if(listBeb) listBeb.innerHTML = bebidasActivas.map(b => `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><span class="text-[11px] text-zinc-300 tracking-widest uppercase font-bold">${b}</span><button type="button" onclick="eliminarBebida('${b}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`).join('');
    
    const nsuc = document.getElementById('nuevo-barbero-sucursal');
    if(nsuc) nsuc.innerHTML = sucursalesActivas.map(s => `<option value="${s}">${s}</option>`).join('');
    
    actualizarMenuSucursalesHeader(); 
    actualizarSelectsForm();
    
    const selProd = document.getElementById('producto-item');
    if(selProd) selProd.innerHTML = '<option value="">+ Producto...</option>' + productosActivos.sort().map(x => `<option value="${x}">${x}</option>`).join('');
}"""
c = c.replace(old_listas, new_listas)


# 2. Update Delete and Form listeners
old_listeners = """window.eliminarSucursal = function(nombre) { sucursalesActivas = sucursalesActivas.filter(s => s !== nombre); actualizarTodasLasListas(); }
window.eliminarBarbero = function(nombre) { barberosActivos = barberosActivos.filter(b => b.nombre !== nombre); actualizarTodasLasListas(); }
window.eliminarServicio = function(nombre) { serviciosActivos = serviciosActivos.filter(s => s !== nombre); actualizarTodasLasListas(); }
window.eliminarBebida = function(nombre) { bebidasActivas = bebidasActivas.filter(b => b !== nombre); actualizarTodasLasListas(); }

document.getElementById('form-nueva-sucursal').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-sucursal-nombre').value.trim(); if(v && !sucursalesActivas.includes(v)) { sucursalesActivas.push(v); document.getElementById('nueva-sucursal-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-barbero').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-barbero-nombre').value.trim(); const suc = document.getElementById('nuevo-barbero-sucursal').value; if(v && !barberosActivos.some(b => b.nombre === v)) { barberosActivos.push({nombre: v, sucursal: suc}); document.getElementById('nuevo-barbero-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-servicio').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-servicio-nombre').value.trim(); const p = parseFloat(document.getElementById('nuevo-servicio-precio').value) || 0; if(v && !serviciosActivos.includes(v)) { preciosBase[v] = p; serviciosActivos.push(v); document.getElementById('nuevo-servicio-nombre').value=''; document.getElementById('nuevo-servicio-precio').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nueva-bebida').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-bebida-nombre').value.trim(); if(v && !bebidasActivas.includes(v)) { bebidasActivas.push(v); document.getElementById('nueva-bebida-nombre').value=''; actualizarTodasLasListas(); }});"""


new_listeners = """window.eliminarProducto = function(nombre) { productosActivos = productosActivos.filter(s => s !== nombre); actualizarTodasLasListas(); }
window.eliminarBarbero = function(nombre) { barberosActivos = barberosActivos.filter(b => b.nombre !== nombre); actualizarTodasLasListas(); }
window.eliminarServicio = function(nombre) { serviciosActivos = serviciosActivos.filter(s => s !== nombre); actualizarTodasLasListas(); }
window.eliminarBebida = function(nombre) { bebidasActivas = bebidasActivas.filter(b => b !== nombre); actualizarTodasLasListas(); }

if (document.getElementById('form-nuevo-producto')) {
    document.getElementById('form-nuevo-producto').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-producto-nombre').value.trim(); const p = parseFloat(document.getElementById('nuevo-producto-precio').value) || 0; if(v && !productosActivos.includes(v)) { preciosBase[v] = p; productosActivos.push(v); document.getElementById('nuevo-producto-nombre').value=''; document.getElementById('nuevo-producto-precio').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nuevo-barbero')) {
    document.getElementById('form-nuevo-barbero').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-barbero-nombre').value.trim(); const suc = document.getElementById('nuevo-barbero-sucursal').value; if(v && !barberosActivos.some(b => b.nombre === v)) { barberosActivos.push({nombre: v, sucursal: suc}); document.getElementById('nuevo-barbero-nombre').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nuevo-servicio')) {
    document.getElementById('form-nuevo-servicio').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-servicio-nombre').value.trim(); const p = parseFloat(document.getElementById('nuevo-servicio-precio').value) || 0; if(v && !serviciosActivos.includes(v)) { preciosBase[v] = p; serviciosActivos.push(v); document.getElementById('nuevo-servicio-nombre').value=''; document.getElementById('nuevo-servicio-precio').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nueva-bebida')) {
    document.getElementById('form-nueva-bebida').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-bebida-nombre').value.trim(); if(v && !bebidasActivas.includes(v)) { bebidasActivas.push(v); document.getElementById('nueva-bebida-nombre').value=''; actualizarTodasLasListas(); }});
}"""
c = c.replace(old_listeners, new_listeners)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("JS modified to handle products correctly.")
