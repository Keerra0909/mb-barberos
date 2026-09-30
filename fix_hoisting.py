import re, time

js = open('app.js', 'r', encoding='utf-8').read()

js = js.replace("""window.toggleMixto = function(isMixto) {""", """function toggleMixto(isMixto) {""")
js = js.replace("""window.calcularRestanteMixto = function() {""", """function calcularRestanteMixto() {""")

js = js.replace("""}

const montoEl = document.getElementById('monto');""", """}
window.toggleMixto = toggleMixto;

const montoEl = document.getElementById('monto');""")

js = js.replace("""}

const regForm = document.getElementById('registro-form');""", """}
window.calcularRestanteMixto = calcularRestanteMixto;

const regForm = document.getElementById('registro-form');""")

open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
