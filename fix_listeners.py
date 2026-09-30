import re
import time

js = open('app.js', 'r', encoding='utf-8').read()

# 1. Update the event listeners to be wrapped in if(...) to avoid null property errors.
# Also update the barbero listener to handle {nombre, sucursal} format and add producto listener.

target_listeners = """document.getElementById('form-nueva-sucursal').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-sucursal-nombre').value.trim(); if(v && !sucursalesActivas.includes(v)) { sucursalesActivas.push(v); document.getElementById('nueva-sucursal-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-barbero').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-barbero-nombre').value.trim(); if(v && !barberosActivos.includes(v)) { barberosActivos.push(v); document.getElementById('nuevo-barbero-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-servicio').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-servicio-nombre').value.trim(); if(v && !serviciosActivos.includes(v)) { serviciosActivos.push(v); document.getElementById('nuevo-servicio-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nueva-bebida').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-bebida-nombre').value.trim(); if(v && !bebidasActivas.includes(v)) { bebidasActivas.push(v); document.getElementById('nueva-bebida-nombre').value=''; actualizarTodasLasListas(); }});"""

safe_listeners = """if (document.getElementById('form-nuevo-producto')) {
    document.getElementById('form-nuevo-producto').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-producto-nombre').value.trim(); const p = parseFloat(document.getElementById('nuevo-producto-precio').value) || 0; if(v && !productosActivos.includes(v)) { preciosBase[v] = p; productosActivos.push(v); document.getElementById('nuevo-producto-nombre').value=''; document.getElementById('nuevo-producto-precio').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nuevo-barbero')) {
    document.getElementById('form-nuevo-barbero').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-barbero-nombre').value.trim(); const suc = document.getElementById('nuevo-barbero-sucursal') ? document.getElementById('nuevo-barbero-sucursal').value : sucursalesActivas[0]; if(v && !barberosActivos.some(b => typeof b === 'string' ? b === v : b.nombre === v)) { barberosActivos.push({nombre: v, sucursal: suc}); document.getElementById('nuevo-barbero-nombre').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nuevo-servicio')) {
    document.getElementById('form-nuevo-servicio').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-servicio-nombre').value.trim(); const p = parseFloat(document.getElementById('nuevo-servicio-precio') ? document.getElementById('nuevo-servicio-precio').value : '0') || 0; if(v && !serviciosActivos.includes(v)) { preciosBase[v] = p; serviciosActivos.push(v); document.getElementById('nuevo-servicio-nombre').value=''; if(document.getElementById('nuevo-servicio-precio')) document.getElementById('nuevo-servicio-precio').value=''; actualizarTodasLasListas(); }});
}
if (document.getElementById('form-nueva-bebida')) {
    document.getElementById('form-nueva-bebida').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-bebida-nombre').value.trim(); if(v && !bebidasActivas.includes(v)) { bebidasActivas.push(v); document.getElementById('nueva-bebida-nombre').value=''; actualizarTodasLasListas(); }});
}"""

if target_listeners in js:
    js = js.replace(target_listeners, safe_listeners)
    print("Replaced listeners successfully.")
else:
    print("Failed to replace listeners. Trying regex.")
    # More robust replace if spaces are slightly off
    js = re.sub(r"document\.getElementById\('form-nueva-sucursal'\)\.addEventListener.*?actualizarTodasLasListas\(\);\s*\}\);", safe_listeners, js, flags=re.DOTALL)
    print("Used regex for listeners.")


# 2. Fix the eliminar functions to properly use objects
target_eliminar = """function eliminarSucursal(n) { mostrarConfirmacion('Eliminar Sucursal', `AEliminar ${n}?`, () => { sucursalesActivas = sucursalesActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarBarbero(n) { mostrarConfirmacion('Eliminar Barbero', `AEliminar a ${n}?`, () => { barberosActivos = barberosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarServicio(n) { mostrarConfirmacion('Eliminar Servicio', `AEliminar ${n}?`, () => { serviciosActivos = serviciosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarBebida(n) { mostrarConfirmacion('Eliminar Bebida', `AEliminar ${n}?`, () => { bebidasActivas = bebidasActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }"""
# Since it has A which is a unicode artifact, use regex instead!

eliminar_regex = re.compile(r'function eliminarSucursal\(n\).*?actualizarTodasLasListas\(\);\s*}\);\s*}', re.DOTALL)

safe_eliminar = """window.eliminarProducto = function(n) { mostrarConfirmacion('Eliminar Producto', `¿Eliminar ${n}?`, () => { productosActivos = productosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
window.eliminarSucursal = function(n) { mostrarConfirmacion('Eliminar Sucursal', `¿Eliminar ${n}?`, () => { sucursalesActivas = sucursalesActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }
window.eliminarBarbero = function(n) { mostrarConfirmacion('Eliminar Barbero', `¿Eliminar a ${n}?`, () => { barberosActivos = barberosActivos.filter(b => typeof b === 'string' ? b !== n : b.nombre !== n); actualizarTodasLasListas(); }); }
window.eliminarServicio = function(n) { mostrarConfirmacion('Eliminar Servicio', `¿Eliminar ${n}?`, () => { serviciosActivos = serviciosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
window.eliminarBebida = function(n) { mostrarConfirmacion('Eliminar Bebida', `¿Eliminar ${n}?`, () => { bebidasActivas = bebidasActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }"""

js = re.sub(eliminar_regex, safe_eliminar, js)

open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
