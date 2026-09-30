import re

c = open('index.html', 'r', encoding='utf-8').read()

# 1. Make sure charset meta is right at the top of <head>
if 'charset="UTF-8"' not in c and "charset='UTF-8'" not in c:
    c = c.replace('<head>', '<head>\n    <meta charset="UTF-8">', 1)

# 2. Add tabla-nomina-barberos before tabla-historial-pagos if missing
if 'tabla-nomina-barberos' not in c:
    c = c.replace(
        '<tbody id="tabla-historial-pagos"',
        '<tbody id="tabla-nomina-barberos" class="divide-y divide-zinc-900"></tbody>\n                                </table>\n                            </div>\n\n                            <!-- historial pagos -->\n                            <table class="w-full text-left text-xs">\n                                <tbody id="tabla-historial-pagos"'
    )
    print("Added tabla-nomina-barberos")
else:
    print("tabla-nomina-barberos already exists")

# 3. Add btn-generar listener anchor if missing
if 'btn-generar' not in c:
    print("WARNING: btn-generar not in HTML")

open('index.html', 'w', encoding='utf-8').write(c)
print('done')
