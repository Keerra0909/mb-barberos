import time, re

# Update app.js
js = open('app.js', 'r', encoding='utf-8').read()

old_func = """window.cambiarSucursal = function(sucursal) { 
    sucursalActual = sucursal; 
    actualizarVistaHoy(); 
    actualizarSelectsForm(); 
}"""

new_func = """window.cambiarSucursal = function(sucursal) { 
    sucursalActual = sucursal; 
    actualizarVistaHoy(); 
    actualizarReportes(); // Add this line to update the reports dynamically
    actualizarSelectsForm(); 
}"""

js = js.replace(old_func, new_func)
open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Report updates fixed on branch change.")
