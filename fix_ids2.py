import re, time

js = open('app.js', 'r', encoding='utf-8').read()
html = open('index.html', 'r', encoding='utf-8').read()

# tabla-pos -> doesn't exist, but vista-pos does
# view-pos -> vista-pos
# view-reportes -> vista-reportes

id_map = {
    'view-pos': 'vista-pos',
    'view-reportes': 'vista-reportes',
    'tabla-pos': 'tabla-registros',  # tabla-registros is the actual ID
}

for old, new in id_map.items():
    # Check if new exists in HTML
    if f'id="{new}"' in html or f"id='{new}'" in html:
        count = js.count(f"'{old}'") + js.count(f'"{old}"')
        js = js.replace(f"'{old}'", f"'{new}'")
        js = js.replace(f'"{old}"', f'"{new}"')
        print(f"Fixed '{old}' -> '{new}': {count} occurrences")
    else:
        print(f"WARNING: '{new}' also not in HTML!")

# Also wrap any remaining getElementById calls that might be null
# For safety: wrap the iniciarSesion and cerrarSesion to guard all critical ones
# The key ones that crash without guards: panelComisiones, etiquetaRol, contenedor-tabs, etc.

critical_ids_check = ['pantalla-login', 'main-app', 'btn-config', 'contenedor-tabs', 
                       'contenedor-sucursal', 'btn-limpiar', 'etiqueta-rol', 'texto-rol',
                       'panel-comisiones', 'label-bitacora-sucursal', 'label-sucursal-form',
                       'filtro-fecha-pos', 'tabla-registros', 'vista-pos', 'vista-reportes']

print("\nChecking critical IDs exist in index.html:")
for cid in critical_ids_check:
    exists = f'id="{cid}"' in html or f"id='{cid}'" in html
    status = "OK" if exists else "MISSING"
    print(f"  {status}: {cid}")

open('app.js', 'w', encoding='utf-8').write(js)

idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("\nDone.")
