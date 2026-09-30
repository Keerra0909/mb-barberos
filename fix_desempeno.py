c = open('app.js', 'r', encoding='utf-8').read()

# 1. Add actualizarDesempenoPos call right after total-cortes line
old = "document.getElementById('total-cortes').textContent = regsHoy.length;\n}"
new = "document.getElementById('total-cortes').textContent = regsHoy.length;\n    actualizarDesempenoPos(regsHoy);\n}"
c = c.replace(old, new, 1)

# 2. After cambiarSucursal in verificarPin, also call actualizarMenuSucursalesHeader
old2 = "cambiarSucursal(sucursalIntentada);\n        \n        document.getElementById('pantalla-login')"
new2 = "cambiarSucursal(sucursalIntentada);\n        actualizarMenuSucursalesHeader();\n        \n        document.getElementById('pantalla-login')"
c = c.replace(old2, new2, 1)

open('app.js', 'w', encoding='utf-8').write(c)

# Verify
assert 'actualizarDesempenoPos(regsHoy)' in c, 'actualizarDesempenoPos call MISSING'
assert c.count('actualizarMenuSucursalesHeader()') >= 2, 'actualizarMenuSucursalesHeader not called on login'
print('done')
print('desempeno calls:', c.count('actualizarDesempenoPos'))
print('header menu calls:', c.count('actualizarMenuSucursalesHeader'))
