import time, re

c = open('index.html', 'r', encoding='utf-8', errors='replace').read()

# Replace the specific grid inside registro-form
# We will use regex to find the grid containing 'Servicio' and 'Cortes'
pattern = re.compile(r'<div class="grid grid-cols-2 gap-4">\s*<div>\s*<label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>.*?<select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>\s*</div>\s*</div>', re.DOTALL)

new_block = """<div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                    <div id="servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Producto / Cortesía</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-1/2 input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Producto</option>
                                        </select>
                                        <select id="bebida" class="w-1/2 input-dark rounded-sm p-3 text-xs"></select>
                                    </div>
                                    <button type="button" onclick="agregarProducto()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Añadir Producto</button>
                                </div>
                            </div>"""

c = re.sub(pattern, new_block, c)

# Let's also fix the settings UI which I might have failed to replace.
# Looking for <!-- Sucursales --> and the whole block up to <!-- Barberos -->
settings_pattern = re.compile(r'<!-- Sucursales -->.*?<!-- Barberos -->', re.DOTALL)
new_settings = """<!-- Productos -->
                <div class="flex flex-col">
                    <h4 class="text-xs text-zinc-400 font-semibold uppercase tracking-widest mb-4 text-center border-b border-zinc-800 pb-2">Productos</h4>
                    <form id="form-nuevo-producto" class="flex flex-col gap-2 mb-4">
                        <input type="text" id="nuevo-producto-nombre" placeholder="Nombre (ej. Cera)" class="w-full text-xs input-dark rounded-sm p-2 border-zinc-800" required>
                        <div class="flex gap-2">
                            <input type="number" id="nuevo-producto-precio" placeholder="Precio $" class="w-full text-xs input-dark rounded-sm p-2 border-zinc-800" required>
                            <button type="submit" class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-4 rounded-sm border border-zinc-700 transition-colors"><i class="fa-solid fa-plus text-xs"></i></button>
                        </div>
                    </form>
                    <div class="border border-zinc-800 bg-[#050505] rounded-sm flex-1 min-h-[200px] overflow-y-auto" id="lista-productos-modal"></div>
                </div>

                <!-- Barberos -->"""

c = re.sub(settings_pattern, new_settings, c)

# Fix corrupted characters
c = c.replace('Cortesa', 'Cortesía')
c = c.replace('Aadir', 'Añadir')
c = c.replace('Nmina', 'Nómina')

open('index.html', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Forced HTML injection using Regex.")
