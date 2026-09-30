import time, re

c = open('index.html', 'r', encoding='utf-8').read()

# Fix the form layout using Regex to grab from "Servicio" grid to "Propina" grid
pattern = re.compile(r'<div class="grid grid-cols-2 gap-4">\s*<div>\s*<label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>.*?<input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm" required>\s*</div>\s*</div>', re.DOTALL)

new_html = """<div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                    <div id="servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Productos</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-full input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Añadir Producto</option>
                                        </select>
                                        <button type="button" onclick="agregarProducto()" class="bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-300 px-3 rounded-sm text-xs transition-colors"><i class="fa-solid fa-plus"></i></button>
                                    </div>
                                </div>
                            </div>
                            <div class="grid grid-cols-3 gap-3">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                                    <input type="number" id="monto" value="380" class="w-full input-dark rounded-sm p-3 text-sm font-bold" required>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                                    <input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm" required>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                                    <select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                </div>
                            </div>"""

c = re.sub(pattern, new_html, c)
open('index.html', 'w', encoding='utf-8').write(c)


js = open('app.js', 'r', encoding='utf-8').read()

# Fix `actualizarSelectsForm` missing the selProd injection
# We will append the selProd injection to the end of the function using regex
fn_pattern = re.compile(r'(function actualizarSelectsForm\(\) \{.*?if\(nsuc\) nsuc\.innerHTML = optBarberos;)?(\s*if\(sBarbero\) sBarbero\.innerHTML = optBarberos;.*?)\}', re.DOTALL)

def inject_selProd(match):
    return match.group(0).rstrip('}') + """
    const selProd = document.getElementById('producto-item');
    if(selProd) selProd.innerHTML = '<option value="">+ Añadir Producto...</option>' + productosActivos.sort().map(x => `<option value="${x}">${x} - $${preciosBase[x]||0}</option>`).join('');
}"""

js = re.sub(fn_pattern, inject_selProd, js)

# Fix adding product logic
js = js.replace("const s = document.getElementById('producto-item').value;", "const sel = document.getElementById('producto-item'); const s = sel.value;")

# Make sure window.agregarProducto exists and resets select
if "window.agregarProducto =" not in js:
    js += """\nwindow.agregarProducto = function() {
        const sel = document.getElementById('producto-item');
        const s = sel.value;
        if(s && !serviciosActuales.includes(s)) {
            serviciosActuales.push(s);
            const currentTotal = parseFloat(document.getElementById('monto').value) || 0;
            document.getElementById('monto').value = currentTotal + (preciosBase[s] || 0);
            actualizarUISeleccion();
            calcularRestanteMixto();
        }
        if(sel) sel.value = '';
    };\n"""

open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Layout restructured and Producto selector populated.")
