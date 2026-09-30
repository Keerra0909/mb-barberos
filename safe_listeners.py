import re
import time

js = open('app.js', 'r', encoding='utf-8').read()

# We want to find: document.getElementById('X').addEventListener('Y', ...)
# and replace with:
# { const el = document.getElementById('X'); if(el) el.addEventListener('Y', ...) }
# But we have to be careful with multi-line statements.
# Let's just do it manually for the known ones at the top level!

# The ones causing issues:
known_ids = [
    'btn-confirm-cancel',
    'btn-confirm-ok',
    'btn-config',
    'btn-cerrar-modal',
    'sucursal-select',
    'filtro-fecha-pos',
    'monto',
    'propina',
    'registro-form',
    'btn-limpiar',
    'tab-pos',
    'tab-reportes',
    'reporte-desde',
    'reporte-hasta',
    'btn-filtrar-reportes',
    'btn-theme',
    'form-pago-barbero',
    'form-gasto',
    'corte-real',
    'form-corte'
]

for kid in known_ids:
    # Look for document.getElementById('kid').addEventListener(...)
    # We will use regex to capture the statement.
    pattern = rf"document\.getElementById\('{kid}'\)\.addEventListener\("
    replacement = rf"if(document.getElementById('{kid}')) document.getElementById('{kid}').addEventListener("
    js = re.sub(pattern, replacement, js)

open('app.js', 'w', encoding='utf-8').write(js)

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("Wrapped all event listeners!")
