import re

c = open('index.html', 'r', encoding='utf-8').read()

fixes = {
    'CortesAa': 'Cortesía',
    'CortesAas': 'Cortesías',
    'AAadir': 'Añadir',
    'NA3mina': 'Nómina',
    'Borrar DAAa': 'Borrar Día',
    'Borrar DÃ\xada': 'Borrar Día',
    'Borrar D\u00c3\u00ada': 'Borrar Día',
    'Borrar DÃ\x83Â\xada': 'Borrar Día',
    'Borrar DA\xada': 'Borrar Día',
    'Borrar DÃ\u00ada': 'Borrar Día',
    'DesempeAo': 'Desempeño',
    'sesiAA3n': 'sesión',
    'especAA-fico': 'específico',
    'TransAcciAnes': 'Transacciones',
}

for old, new in fixes.items():
    c = c.replace(old, new)

# Let's forcefully replace any lingering bad 'Borrar' text just in case:
c = re.sub(r'Borrar D.*a', 'Borrar Día', c)

open('index.html', 'w', encoding='utf-8').write(c)

# Also fix app.js bad chars
js_c = open('app.js', 'r', encoding='utf-8').read()
for old, new in fixes.items():
    js_c = js_c.replace(old, new)

# And fix the specific alert
js_c = re.sub(r"alert\('Selecciona una sucursal en espec.*?fico arriba.'\)", "alert('Selecciona una sucursal en específico arriba.')", js_c)
js_c = re.sub(r"switchTab\('pos'\); // Siempre forzar a POS al iniciar sesi.*?n", "switchTab('pos'); // Siempre forzar a POS al iniciar sesión", js_c)

open('app.js', 'w', encoding='utf-8').write(js_c)

print('Done fixing encodings.')
