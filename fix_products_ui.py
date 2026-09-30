import time, re

c = open('index.html', 'r', encoding='utf-8', errors='ignore').read()

# Fix encoding issues that might have happened
c = c.replace('Cortesa', 'Cortesía')
c = c.replace('CortesAa', 'Cortesía')
c = c.replace('Aadir', 'Añadir')
c = c.replace('AEn quAc se gastA3?', '¿En qué se gastó?')

# 1. Inject the Producto dropdown into the Nuevo Ticket form
old_servicio = """                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                                    <select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                                </div>
                            </div>
                            <div class="pt-2">"""

new_servicio = """                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Producto / Cortesía</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-1/2 input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Producto</option>
                                        </select>
                                        <select id="bebida" class="w-1/2 input-dark rounded-sm p-3 text-xs"></select>
                                    </div>
                                    <button type="button" onclick="agregarProducto()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Añadir Producto</button>
                                </div>
                            </div>
                            <div class="pt-2">"""

c = c.replace(old_servicio, new_servicio)

# 2. Modify Settings Modal: Remove Sucursales, Add Productos
old_settings = """            <div class="p-6 overflow-y-auto grid grid-cols-1 md:grid-cols-4 gap-8">
                <!-- Sucursales -->
                <div class="flex flex-col">
                    <h4 class="text-xs text-zinc-400 font-semibold uppercase tracking-widest mb-4 text-center border-b border-zinc-800 pb-2">Sucursales</h4>
                    <form id="form-nueva-sucursal" class="flex gap-2 mb-4">
                        <input type="text" id="nueva-sucursal-nombre" placeholder="Añadir..." class="w-full text-xs input-dark rounded-sm p-2 border-zinc-800" required>
                        <button type="submit" class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-3 rounded-sm border border-zinc-700 transition-colors"><i class="fa-solid fa-plus text-xs"></i></button>
                    </form>
                    <div class="border border-zinc-800 bg-[#050505] rounded-sm flex-1 min-h-[200px] overflow-y-auto" id="lista-sucursales-modal"></div>
                </div>

                <!-- Barberos -->"""

new_settings = """            <div class="p-6 overflow-y-auto grid grid-cols-1 md:grid-cols-4 gap-8">
                <!-- Productos -->
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

c = c.replace(old_settings, new_settings)

# Write index.html
open('index.html', 'w', encoding='utf-8').write(c)
print("HTML modified for products UI and settings")
