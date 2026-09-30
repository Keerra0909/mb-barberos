import time, re

js = open('app.js', 'r', encoding='utf-8').read()

new_vars = """let preciosBase = {
    'Corte de Cabello': 220, 'Corte de Barba (Ritual)': 220, 'Corte y Barba': 380, 'Servicio Express': 120, 'Servicio Luxury': 550,
    'Limpieza Facial': 180, 'Facial y Corte': 330, 'Facial, Corte y Barba': 480, 'Facial y Barba': 330,
    'Corte y Masaje': 600, 'Corte, Barba y Masaje': 750, 'Corte y Reflexoterapia': 580, 'Corte, Barba y Reflexoterapia': 730,
    'Tinte de Barba': 120, 'Grecas': 80, 'Perfilado de Cejas': 80, 'Planchado de Cejas': 150,
    // Productos Físicos
    'Pomada Mate': 250, 'Pomada Brillo': 250, 'Polvo Texturizador': 180, 'Minoxidil': 350, 'Aceite para Barba': 150, 'Cerveza Extra': 50
};
let productosActivos = ['Pomada Mate', 'Pomada Brillo', 'Polvo Texturizador', 'Minoxidil', 'Aceite para Barba', 'Cerveza Extra'];
let cortesCaja = [];
"""

if "let preciosBase" not in js:
    # insert after let bebidasActivas ...
    target = "let bebidasActivas = ['-', 'Agua', 'Coca Cola', 'Cerveza', 'Jugo'];"
    if target in js:
        js = js.replace(target, target + "\n" + new_vars)
        print("Injected globals!")
    else:
        print("Target for injection not found!")

open('app.js', 'w', encoding='utf-8').write(js)

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
