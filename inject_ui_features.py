import time, re

c = open('index.html', 'r', encoding='utf-8').read()

# 1. Add "Gasto" and "Corte de Caja" buttons to the header of the "Nuevo Ticket" panel
old_header = """<div class="flex justify-between items-center mb-6 border-b border-zinc-800 pb-4">
                            <h2 class="text-sm font-sans font-bold silver-text tracking-widest uppercase">Nuevo Ticket</h2>"""
new_header = """<div class="flex flex-wrap gap-2 justify-between items-center mb-6 border-b border-zinc-800 pb-4">
                            <div class="flex items-center gap-3">
                                <h2 class="text-sm font-sans font-bold silver-text tracking-widest uppercase">Nuevo Ticket</h2>
                                <button type="button" onclick="abrirModalGasto()" class="text-[9px] bg-red-950 text-red-400 border border-red-900 hover:bg-red-900 px-2 py-1.5 rounded-sm transition-colors uppercase tracking-widest font-bold">+ GASTO</button>
                                <button type="button" onclick="abrirModalCorteCaja()" class="text-[9px] bg-yellow-950 text-yellow-400 border border-yellow-900 hover:bg-yellow-900 px-2 py-1.5 rounded-sm transition-colors uppercase tracking-widest font-bold">CORTE CAJA</button>
                            </div>"""
c = c.replace(old_header, new_header)

# 2. Add "Producto" selector next to "Servicio"
old_servicio = """                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <div class="flex gap-2">
                                        <select id="servicio-cat" class="w-2/5 input-dark rounded-sm p-3 text-xs" onchange="actualizarOpcionesServicio()"></select>
                                        <select id="servicio-item" class="w-3/5 input-dark rounded-sm p-3 text-xs font-bold text-white"></select>
                                    </div>
                                    <button type="button" onclick="agregarServicio()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Añadir Servicio</button>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                                    <select id="bebida" class="w-full input-dark rounded-sm p-3 text-sm">
                                        <option value="-">Ninguna</option>
                                        <option value="Agua">Agua</option>
                                        <option value="Coca Cola">Coca Cola</option>
                                        <option value="Cerveza">Cerveza</option>
                                        <option value="Jugo">Jugo</option>
                                    </select>
                                </div>
                            </div>
                            <!-- Tags de servicios seleccionados -->
                            <div id="servicios-seleccionados" class="flex flex-wrap gap-2 empty:hidden"></div>"""

new_servicio = """                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                                    <div class="flex gap-2">
                                        <select id="servicio-cat" class="w-2/5 input-dark rounded-sm p-3 text-xs" onchange="actualizarOpcionesServicio()"></select>
                                        <select id="servicio-item" class="w-3/5 input-dark rounded-sm p-3 text-xs font-bold text-white"></select>
                                    </div>
                                    <button type="button" onclick="agregarServicio()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Añadir Servicio</button>
                                </div>
                                <div>
                                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Producto / Cortesía</label>
                                    <div class="flex gap-2">
                                        <select id="producto-item" class="w-1/2 input-dark rounded-sm p-3 text-xs font-bold text-zinc-300">
                                            <option value="">+ Producto</option>
                                        </select>
                                        <select id="bebida" class="w-1/2 input-dark rounded-sm p-3 text-xs">
                                            <option value="-">Cortesía...</option>
                                            <option value="Agua">Agua</option>
                                            <option value="Coca Cola">Coca Cola</option>
                                            <option value="Cerveza">Cerveza</option>
                                            <option value="Jugo">Jugo</option>
                                        </select>
                                    </div>
                                    <button type="button" onclick="agregarProducto()" class="mt-2 w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 p-2 rounded-sm text-[10px] uppercase tracking-widest transition-colors">+ Añadir Producto</button>
                                </div>
                            </div>
                            <!-- Tags de servicios seleccionados -->
                            <div id="servicios-seleccionados" class="flex flex-wrap gap-2 empty:hidden"></div>"""

c = c.replace(old_servicio, new_servicio)

# 3. Add Modals for Gasto and Corte at the end of the body
modals = """
    <!-- Modal Gasto -->
    <div id="modal-gasto" class="fixed inset-0 bg-[#050505]/90 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-panel w-full max-w-sm rounded-sm p-6 relative">
            <h3 class="text-lg font-sans font-bold text-red-500 tracking-widest uppercase mb-4 border-b border-zinc-800 pb-3">Registrar Gasto</h3>
            <form id="form-gasto" class="space-y-4">
                <div>
                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Concepto (¿En qué se gastó?)</label>
                    <input type="text" id="gasto-concepto" class="w-full input-dark rounded-sm p-3 text-sm" placeholder="Ej. Garrafones de agua" required>
                </div>
                <div>
                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                    <input type="number" id="gasto-monto" class="w-full input-dark rounded-sm p-3 text-sm font-bold text-red-400" required>
                </div>
                <div class="pt-4 flex gap-3">
                    <button type="button" onclick="cerrarModalGasto()" class="flex-1 border border-zinc-700 text-zinc-400 hover:text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors">Cancelar</button>
                    <button type="submit" class="flex-1 bg-red-600 hover:bg-red-700 text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors shadow-lg">Registrar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal Corte de Caja -->
    <div id="modal-corte" class="fixed inset-0 bg-[#050505]/90 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="glass-panel w-full max-w-md rounded-sm p-6 relative border-t-2 border-yellow-500">
            <h3 class="text-lg font-sans font-bold text-yellow-500 tracking-widest uppercase mb-4 border-b border-zinc-800 pb-3">Corte de Caja (Fin de Turno)</h3>
            <div class="space-y-4 mb-6">
                <div class="flex justify-between items-center text-sm border-b border-zinc-800/50 pb-2">
                    <span class="text-zinc-400 uppercase tracking-widest text-xs">Ingresos en Efectivo:</span>
                    <span id="corte-ingresos-efvo" class="font-mono text-emerald-400 font-bold"></span>
                </div>
                <div class="flex justify-between items-center text-sm border-b border-zinc-800/50 pb-2">
                    <span class="text-zinc-400 uppercase tracking-widest text-xs">Gastos Totales (-):</span>
                    <span id="corte-gastos" class="font-mono text-red-400 font-bold"></span>
                </div>
                <div class="flex justify-between items-center text-sm border-b border-zinc-700 pb-2">
                    <span class="text-zinc-200 uppercase tracking-widest text-[11px] font-bold">Total Esperado en Cajón:</span>
                    <span id="corte-esperado" class="font-mono text-white text-lg font-bold"></span>
                </div>
            </div>
            
            <form id="form-corte" class="space-y-4">
                <div class="bg-yellow-950/20 border border-yellow-900/50 p-4 rounded-sm">
                    <label class="block text-[11px] text-yellow-500 font-semibold mb-2 uppercase tracking-widest">¿Cuánto efectivo hay físicamente?</label>
                    <input type="number" id="corte-real" class="w-full bg-black border border-yellow-700/50 rounded-sm p-3 text-lg font-bold text-white text-center" placeholder="$0.00" required>
                </div>
                <div id="corte-diferencia-box" class="hidden text-center text-sm font-bold uppercase tracking-widest p-2 rounded-sm border"></div>
                <div class="pt-4 flex gap-3">
                    <button type="button" onclick="cerrarModalCorteCaja()" class="flex-1 border border-zinc-700 text-zinc-400 hover:text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors">Cancelar</button>
                    <button type="submit" class="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors shadow-lg">Cerrar Turno</button>
                </div>
            </form>
        </div>
    </div>
"""
if "modal-gasto" not in c:
    c = c.replace('</body>', modals + '\n</body>')

open('index.html', 'w', encoding='utf-8').write(c)
print("HTML injected for products, expenses, and cash closing.")
