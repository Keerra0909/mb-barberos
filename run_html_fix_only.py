import time, re

c = open('index.html', 'r', encoding='utf-8').read()

old_form_block = """                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                    <div id="servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Producto / Cortesa</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-1/2 input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Producto</option>
                                        </select>
                                        <select id="bebida" class="w-1/2 input-dark rounded-sm p-3 text-xs"></select>
                                    </div>
                                    <button type="button" onclick="agregarProducto()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Aadir Producto</button>
                                </div>
                            </div>
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                                    <input type="number" id="monto" value="380" class="w-full input-dark rounded-sm p-3 text-sm font-bold" required>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                                    <input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm">
                                </div>
                            </div>"""

old_form_block_utf8 = old_form_block.replace('Cortesa', 'Cortesía').replace('Aadir', 'Añadir')


new_form_block = """                            <div class="grid grid-cols-2 gap-4">
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
                                    <input type="number" id="propina" value="0" class="w-full input-dark rounded-sm p-3 text-sm">
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                                    <select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                </div>
                            </div>"""

if old_form_block in c:
    c = c.replace(old_form_block, new_form_block)
    print("Replaced ASCII block")
elif old_form_block_utf8 in c:
    c = c.replace(old_form_block_utf8, new_form_block)
    print("Replaced UTF8 block")
else:
    print("WARNING: form block not found!")

old_th = """<th class="p-4 font-normal text-emerald-500 font-bold" title="50% Servicio + Propina">Sueldo / Comisión</th>"""
new_th = """<th class="p-4 font-normal text-emerald-500 font-bold" title="50% Servicio + Propina">Comisión / Propina</th>"""
c = c.replace(old_th, new_th)

open('index.html', 'w', encoding='utf-8').write(c)
