import time, re

c = open('index.html', 'r', encoding='utf-8').read()

# Modify Modal Editar HTML
old_modal = """            <form id="form-editar-ticket" class="p-6 space-y-5 bg-[#09090b]">
                <input type="hidden" id="edit-ticket-id">
                <div>
                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Barbero</label>
                    <select id="edit-barbero" class="w-full input-dark rounded-sm p-3 text-sm" required></select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                        <select id="edit-servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
<div id="edit-servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">CortesAa</label>
                        <select id="edit-bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                        <input type="number" id="edit-monto" class="w-full input-dark rounded-sm p-3 text-sm font-bold" required>
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                        <input type="number" id="edit-propina" class="w-full input-dark rounded-sm p-3 text-sm">
                    </div>
                </div>
                <div class="pt-2">
                    <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Forma de Pago</label>
                    <select id="edit-pago" class="w-full input-dark rounded-sm p-3 text-sm text-center font-bold">
                        <option value="Efectivo">Efectivo</option>
                        <option value="Tarjeta">Tarjeta</option>
                        <option value="Mixto">Mixto</option>
                    </select>
                </div>
                <div class="pt-4 flex gap-3">
                    <button type="button" onclick="cerrarModalEditar()" class="flex-1 border border-zinc-700 text-zinc-400 hover:text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors">Cancelar</button>
                    <button type="submit" class="flex-1 bg-zinc-200 text-black p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors hover:bg-white shadow-lg">Guardar Cambios</button>
                </div>
            </form>"""

# Fix the typo CortesAa as well, just use Cortesía/Bebida
new_modal = """            <form id="form-editar-ticket" class="p-6 bg-[#09090b]">
                <input type="hidden" id="edit-ticket-id">
                
                <div id="edit-fields-ticket" class="space-y-5">
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Barbero</label>
                        <select id="edit-barbero" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Servicio</label>
                            <select id="edit-servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                            <div id="edit-servicios-seleccionados" class="flex flex-wrap gap-2 mt-2 hidden"></div>
                        </div>
                        <div>
                            <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Cortesía</label>
                            <select id="edit-bebida" class="w-full input-dark rounded-sm p-3 text-sm"></select>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                            <input type="number" id="edit-monto" class="w-full input-dark rounded-sm p-3 text-sm font-bold">
                        </div>
                        <div>
                            <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Propina ($)</label>
                            <input type="number" id="edit-propina" class="w-full input-dark rounded-sm p-3 text-sm">
                        </div>
                    </div>
                    <div class="pt-2">
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Forma de Pago</label>
                        <select id="edit-pago" class="w-full input-dark rounded-sm p-3 text-sm text-center font-bold">
                            <option value="Efectivo">Efectivo</option>
                            <option value="Tarjeta">Tarjeta</option>
                            <option value="Mixto">Mixto</option>
                        </select>
                    </div>
                </div>

                <div id="edit-fields-gasto" class="space-y-5 hidden">
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Concepto (Gasto)</label>
                        <input type="text" id="edit-gasto-concepto" class="w-full input-dark rounded-sm p-3 text-sm">
                    </div>
                    <div>
                        <label class="block text-xs text-zinc-400 font-semibold mb-2 uppercase tracking-widest">Monto ($)</label>
                        <input type="number" id="edit-gasto-monto" class="w-full input-dark rounded-sm p-3 text-sm font-bold text-red-400">
                    </div>
                </div>

                <button type="button" id="btn-delete-ticket" onclick="borrarTicketEnEdicion()" class="w-full mt-6 bg-red-950/50 text-red-500 border border-red-900/50 hover:bg-red-900 hover:text-red-100 p-3 rounded-sm text-[10px] font-bold tracking-widest uppercase transition-colors hidden"><i class="fa-solid fa-trash mr-2"></i> Borrar Permanentemente</button>

                <div class="pt-6 flex gap-3">
                    <button type="button" onclick="cerrarModalEditar()" class="flex-1 border border-zinc-700 text-zinc-400 hover:text-white p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors">Cancelar</button>
                    <button type="submit" class="flex-1 bg-zinc-200 text-black p-3 rounded-sm text-xs tracking-widest uppercase font-bold transition-colors hover:bg-white shadow-lg">Guardar Cambios</button>
                </div>
            </form>"""
c = c.replace(old_modal, new_modal)

open('index.html', 'w', encoding='utf-8').write(c)

js = open('app.js', 'r', encoding='utf-8').read()

# Make the Edit button appear for Gastos in the table
old_gasto_td = """                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Caja</span></td>
                <td class="p-3 pr-6"></td>"""
new_gasto_td = """                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Caja</span></td>
                <td class="p-3 pr-6 text-right">
                    <button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-white transition-colors" title="Editar Gasto"><i class="fa-solid fa-pen text-[11px]"></i></button>
                </td>"""
js = js.replace(old_gasto_td, new_gasto_td)


# Update Modal logic in JS
old_abrir = """window.abrirModalEditar = function(id) {
    const reg = registros.find(r => r.id === id);
    if(!reg) return;
    ticketEnEdicion = reg.id;
    document.getElementById('edit-barbero').value = reg.barbero;
    editServiciosActuales = reg.servicio.split(' + ').filter(s => s !== 'Ninguno');
    actualizarUISeleccionEdit();
    document.getElementById('edit-bebida').value = reg.bebida === '-' ? '' : reg.bebida;
    document.getElementById('edit-monto').value = reg.monto;
    document.getElementById('edit-propina').value = reg.propina;
    document.getElementById('edit-pago').value = reg.pagoTxt;
    
    modalEditar.classList.remove('hidden');
}"""

new_abrir = """window.abrirModalEditar = function(id) {
    const reg = registros.find(r => r.id === id);
    if(!reg) return;
    ticketEnEdicion = reg.id;
    
    const btnDel = document.getElementById('btn-delete-ticket');
    if (btnDel) {
        if (rolActual === 'Admin') btnDel.classList.remove('hidden');
        else btnDel.classList.add('hidden');
    }

    if (reg.tipo === 'Gasto') {
        document.getElementById('edit-fields-ticket').classList.add('hidden');
        document.getElementById('edit-fields-gasto').classList.remove('hidden');
        document.getElementById('edit-gasto-concepto').value = reg.servicio;
        document.getElementById('edit-gasto-monto').value = reg.monto;
    } else {
        document.getElementById('edit-fields-ticket').classList.remove('hidden');
        document.getElementById('edit-fields-gasto').classList.add('hidden');
        document.getElementById('edit-barbero').value = reg.barbero;
        editServiciosActuales = reg.servicio.split(' + ').filter(s => s !== 'Ninguno');
        actualizarUISeleccionEdit();
        document.getElementById('edit-bebida').value = reg.bebida === '-' ? '' : reg.bebida;
        document.getElementById('edit-monto').value = reg.monto;
        document.getElementById('edit-propina').value = reg.propina;
        document.getElementById('edit-pago').value = reg.pagoTxt;
    }
    
    modalEditar.classList.remove('hidden');
}

window.borrarTicketEnEdicion = function() {
    if (rolActual !== 'Admin') return; // Safety check
    if(confirm('¿ESTÁS COMPLETAMENTE SEGURO DE BORRAR ESTE REGISTRO? ESTO AFECTARÁ LA CAJA Y LOS REPORTES Y NO SE PUEDE DESHACER.')) {
        registros = registros.filter(r => r.id !== ticketEnEdicion);
        cerrarModalEditar();
        actualizarVistaHoy();
        actualizarReportes();
    }
}
"""
js = js.replace(old_abrir, new_abrir)


# Update form submit to handle both Gasto and Ticket
old_edit_submit = """document.getElementById('form-editar-ticket').addEventListener('submit', (e) => {
    e.preventDefault();
    if(!ticketEnEdicion) return;
    const reg = registros.find(r => r.id === ticketEnEdicion);
    if(reg) {
        reg.barbero = document.getElementById('edit-barbero').value;
        reg.servicio = editServiciosActuales.join(' + ') || 'Ninguno';
        reg.bebida = document.getElementById('edit-bebida').value || '-';
        reg.monto = parseFloat(document.getElementById('edit-monto').value) || 0;
        reg.propina = parseFloat(document.getElementById('edit-propina').value) || 0;
        reg.pagoTxt = document.getElementById('edit-pago').value;
        reg.editado = true;
        
        reg.valEfectivo = reg.pagoTxt === 'Efectivo' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
        reg.valTarjeta = reg.pagoTxt === 'Tarjeta' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
    }
    cerrarModalEditar();
    actualizarVistaHoy();
    actualizarReportes(); // Actualiza admin si estA! abierto
});"""

new_edit_submit = """document.getElementById('form-editar-ticket').addEventListener('submit', (e) => {
    e.preventDefault();
    if(!ticketEnEdicion) return;
    const reg = registros.find(r => r.id === ticketEnEdicion);
    if(reg) {
        if (reg.tipo === 'Gasto') {
            reg.servicio = document.getElementById('edit-gasto-concepto').value;
            reg.monto = parseFloat(document.getElementById('edit-gasto-monto').value) || 0;
        } else {
            reg.barbero = document.getElementById('edit-barbero').value;
            reg.servicio = editServiciosActuales.join(' + ') || 'Ninguno';
            reg.bebida = document.getElementById('edit-bebida').value || '-';
            reg.monto = parseFloat(document.getElementById('edit-monto').value) || 0;
            reg.propina = parseFloat(document.getElementById('edit-propina').value) || 0;
            reg.pagoTxt = document.getElementById('edit-pago').value;
            
            reg.valEfectivo = reg.pagoTxt === 'Efectivo' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
            reg.valTarjeta = reg.pagoTxt === 'Tarjeta' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
        }
        reg.editado = true;
    }
    cerrarModalEditar();
    actualizarVistaHoy();
    actualizarReportes(); 
});"""
js = js.replace(old_edit_submit, new_edit_submit)

open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Edit/Delete for Gastos and Tickets done. Admin only deletion enforced.")
