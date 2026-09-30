import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# 1. Add localStorage persistence back!
# Find the globals declaration
old_globals = """let registros = [];
let pagosNomina = [];
let historialEdiciones = [];
let sucursalesActivas = ['La Morena', 'La Quemada', 'Nativitas'];"""

new_globals = """let registros = JSON.parse(localStorage.getItem('mb_registros')) || [];
let pagosNomina = JSON.parse(localStorage.getItem('mb_pagos')) || [];
let historialEdiciones = JSON.parse(localStorage.getItem('mb_ediciones')) || [];
let sucursalesActivas = ['La Morena', 'La Quemada', 'Nativitas'];

window.guardarDatos = function() {
    localStorage.setItem('mb_registros', JSON.stringify(registros));
    localStorage.setItem('mb_pagos', JSON.stringify(pagosNomina));
    localStorage.setItem('mb_ediciones', JSON.stringify(historialEdiciones));
};"""
js = js.replace(old_globals, new_globals)

# 2. Call guardarDatos after registering a ticket
old_reg = """    actualizarVistaHoy();
});"""
new_reg = """    guardarDatos();
    actualizarVistaHoy();
});"""
js = js.replace(old_reg, new_reg)

# 3. Call guardarDatos after registering a payroll payment (if it exists)
old_pay = """    window.cerrarModalPago();
    actualizarReportes();
});"""
new_pay = """    guardarDatos();
    window.cerrarModalPago();
    actualizarReportes();
});"""
js = js.replace(old_pay, new_pay)

open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
