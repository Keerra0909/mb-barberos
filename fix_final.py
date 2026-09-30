c = open('index.html', 'r', encoding='utf-8').read()

fixes = {
    'tabla-N\u00f3mina-barberos': 'tabla-nomina-barberos',
    'Cortes\u00c3\u00adA': 'Cortesía',   # capital A at end
    'CortesA\u00ads': 'Cortesías',
    'Cortes\u00c3\xada': 'Cortesía',
    'Cortes\u00c3\u00ad\u00adas': 'Cortesías',
    'CortesÃ\xadas': 'Cortesías',
    'CortesÃ­as': 'Cortesías',
    'CortesÃ­a': 'Cortesía',
    'Borrar DA\u00ada': 'Borrar Día',
    'Borrar D\u00c3\u00ada': 'Borrar Día',
    'Borrar DÃ­a': 'Borrar Día',
    'V\u00c3\u00ada de Pago': 'Vía de Pago',
    'VÃ­a de Pago': 'Vía de Pago',
    'pago-M\u00e9todo': 'pago-metodo',
    'pago-Método': 'pago-metodo',
    'Confirmaci\u00c3\u00b3n': 'Confirmación',
    'ConfirmaciÃ³n': 'Confirmación',
    '\u00c2\u00bf': '¿',
    'Est\u00c3\u00a1s': 'Estás',
    'EstÃ¡s': 'Estás',
    'autom\u00c3\u00a1ticamente': 'automáticamente',
    'automÃ¡ticamente': 'automáticamente',
    'col-Acci\u00f3n': 'col-accion',
    'col-Acción': 'col-accion',
}

for old, new in fixes.items():
    c = c.replace(old, new)

open('index.html', 'w', encoding='utf-8').write(c)

# Verify
assert 'tabla-nomina-barberos' in c, 'tabla-nomina-barberos MISSING'
assert 'CortesÃ' not in c, 'CortesÃ still present'
assert 'pago-metodo' in c, 'pago-metodo MISSING'
print('All checks passed')
