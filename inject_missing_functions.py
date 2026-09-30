import time, re

js = open('app.js', 'r', encoding='utf-8').read()

# ==============================================================
# FIX 1: barberosLocal is used in actualizarReportes but never declared.
# We need a helper that normalizes barberosActivos (can be strings or objects)
# ==============================================================
if 'barberosLocal' not in js:
    js = js.replace(
        "    const mapBarberos = {}; \n    const mapNomina = {};",
        """    const barberosLocal = barberosActivos.map(b => typeof b === 'string' ? b : b.nombre);
    const mapBarberos = {}; 
    const mapNomina = {};"""
    )
    print("Injected barberosLocal")

# ==============================================================
# FIX 2: abrirModalLiquidacion is called in the payroll table but never defined
# ==============================================================
if 'abrirModalLiquidacion' not in js:
    liquidacion_fn = """

// ==========================================
// 8. MODAL LIQUIDACIÓN (ALIAS)
// ==========================================
window.abrirModalLiquidacion = function(barbero, saldo) {
    abrirModalPago(barbero, Math.max(0, saldo));
}
"""
    js = js.replace("// ==========================================\n// 9. GASTOS Y CORTE DE CAJA", liquidacion_fn + "\n// ==========================================\n// 9. GASTOS Y CORTE DE CAJA")
    print("Injected abrirModalLiquidacion")

# ==============================================================
# FIX 3: abrirModalEditar - critical for editing/deleting tickets
# ==============================================================
if 'abrirModalEditar' not in js:
    edit_fn = """

// ==========================================
// EDITAR / BORRAR TICKETS (Admin only)
// ==========================================
let ticketEnEdicion = null;
let editServiciosActuales = [];
const modalEditar = document.getElementById('modal-editar');

window.abrirModalEditar = function(id) {
    const reg = registros.find(r => r.id === id);
    if(!reg) return;
    ticketEnEdicion = reg.id;
    
    const btnDel = document.getElementById('btn-delete-ticket');
    if (btnDel) {
        if (rolActual === 'admin') btnDel.classList.remove('hidden');
        else btnDel.classList.add('hidden');
    }

    const fieldsTx = document.getElementById('edit-fields-ticket');
    const fieldsGasto = document.getElementById('edit-fields-gasto');
    
    if (reg.tipo === 'Gasto') {
        if(fieldsTx) fieldsTx.classList.add('hidden');
        if(fieldsGasto) fieldsGasto.classList.remove('hidden');
        if(document.getElementById('edit-gasto-concepto')) document.getElementById('edit-gasto-concepto').value = reg.servicio;
        if(document.getElementById('edit-gasto-monto')) document.getElementById('edit-gasto-monto').value = reg.monto;
    } else {
        if(fieldsTx) fieldsTx.classList.remove('hidden');
        if(fieldsGasto) fieldsGasto.classList.add('hidden');
        if(document.getElementById('edit-barbero')) document.getElementById('edit-barbero').value = reg.barbero;
        editServiciosActuales = reg.servicio ? reg.servicio.split(' + ').filter(s => s !== 'Ninguno') : [];
        if(typeof actualizarUISeleccionEdit === 'function') actualizarUISeleccionEdit();
        if(document.getElementById('edit-bebida')) document.getElementById('edit-bebida').value = reg.bebida === '-' ? '' : (reg.bebida || '');
        if(document.getElementById('edit-monto')) document.getElementById('edit-monto').value = reg.monto;
        if(document.getElementById('edit-propina')) document.getElementById('edit-propina').value = reg.propina;
        if(document.getElementById('edit-pago')) document.getElementById('edit-pago').value = reg.pagoTxt;
    }
    
    if(modalEditar) modalEditar.classList.remove('hidden');
}

window.cerrarModalEditar = function() {
    ticketEnEdicion = null;
    if(modalEditar) modalEditar.classList.add('hidden');
}

window.borrarTicketEnEdicion = function() {
    if (rolActual !== 'admin') return;
    mostrarConfirmacion('Borrar Registro', '¿ESTÁS SEGURO? Esto borrará el ticket de la bitácora y afectará los reportes.', () => {
        registros = registros.filter(r => r.id !== ticketEnEdicion);
        cerrarModalEditar();
        actualizarVistaHoy();
        if(!document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
    });
}

function actualizarUISeleccionEdit() {
    const div = document.getElementById('edit-servicios-seleccionados');
    if(!div) return;
    if(editServiciosActuales.length === 0) { div.classList.add('hidden'); return; }
    div.classList.remove('hidden');
    div.innerHTML = editServiciosActuales.map(s => `<span class="inline-flex items-center gap-1 px-2 py-1 bg-zinc-800 border border-zinc-700 text-zinc-200 text-xs rounded-sm">${s} <button type="button" onclick="quitarServicioEdit('${s}')" class="text-zinc-500 hover:text-red-400">×</button></span>`).join('');
}

window.quitarServicioEdit = function(s) {
    editServiciosActuales = editServiciosActuales.filter(x => x !== s);
    actualizarUISeleccionEdit();
}

window.agregarServicioEdit = function() {
    const sel = document.getElementById('edit-servicio');
    const s = sel ? sel.value : '';
    if(s && !editServiciosActuales.includes(s)) {
        editServiciosActuales.push(s);
        actualizarUISeleccionEdit();
    }
}

if(document.getElementById('form-editar-ticket')) {
    document.getElementById('form-editar-ticket').addEventListener('submit', (e) => {
        e.preventDefault();
        if(!ticketEnEdicion) return;
        const reg = registros.find(r => r.id === ticketEnEdicion);
        if(reg) {
            if (reg.tipo === 'Gasto') {
                reg.servicio = document.getElementById('edit-gasto-concepto') ? document.getElementById('edit-gasto-concepto').value : reg.servicio;
                reg.monto = parseFloat(document.getElementById('edit-gasto-monto') ? document.getElementById('edit-gasto-monto').value : reg.monto) || 0;
            } else {
                reg.barbero = document.getElementById('edit-barbero') ? document.getElementById('edit-barbero').value : reg.barbero;
                reg.servicio = editServiciosActuales.join(' + ') || 'Ninguno';
                reg.bebida = document.getElementById('edit-bebida') ? (document.getElementById('edit-bebida').value || '-') : '-';
                reg.monto = parseFloat(document.getElementById('edit-monto') ? document.getElementById('edit-monto').value : 0) || 0;
                reg.propina = parseFloat(document.getElementById('edit-propina') ? document.getElementById('edit-propina').value : 0) || 0;
                reg.pagoTxt = document.getElementById('edit-pago') ? document.getElementById('edit-pago').value : reg.pagoTxt;
                reg.valEfectivo = reg.pagoTxt === 'Efectivo' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
                reg.valTarjeta = reg.pagoTxt === 'Tarjeta' ? reg.monto : (reg.pagoTxt === 'Mixto' ? reg.monto/2 : 0);
            }
            reg.editado = true;
        }
        cerrarModalEditar();
        actualizarVistaHoy();
        if(!document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
    });
}
"""
    # Insert before section 9
    js = js.replace("// ==========================================\n// 9. GASTOS Y CORTE DE CAJA", edit_fn + "\n// ==========================================\n// 9. GASTOS Y CORTE DE CAJA")
    print("Injected abrirModalEditar and full edit block")

# ==============================================================
# FIX 4: actualizarMenuSucursalesHeader — updates header dropdown
# ==============================================================
if 'actualizarMenuSucursalesHeader' not in js:
    header_fn = """
window.actualizarMenuSucursalesHeader = function() {
    const sel = document.getElementById('sucursal-select');
    if(!sel) return;
    const current = sel.value;
    sel.innerHTML = '';
    [...sucursalesActivas].sort().forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        if(s === current) opt.selected = true;
        sel.appendChild(opt);
    });
}
"""
    js += header_fn
    print("Injected actualizarMenuSucursalesHeader")

# ==============================================================
# FIX 5: actualizarPrecioServicio — used when editing prices inline
# ==============================================================
if 'actualizarPrecioServicio' not in js:
    precio_fn = """
window.actualizarPrecioServicio = function(nombre, valor) {
    preciosBase[nombre] = parseFloat(valor) || 0;
}
"""
    js += precio_fn
    print("Injected actualizarPrecioServicio")

# ==============================================================
# FIX 6: serviciosActuales for new ticket multi-select
# ==============================================================
if 'let serviciosActuales' not in js and 'var serviciosActuales' not in js and 'serviciosActuales' not in js[:500]:
    servicios_actuales = """
let serviciosActuales = [];

window.agregarServicio = function() {
    const sel = document.getElementById('servicio');
    const s = sel ? sel.value : '';
    if(s && !serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        actualizarUISeleccion();
    }
}

function actualizarUISeleccion() {
    const div = document.getElementById('servicios-seleccionados');
    if(!div) return;
    if(serviciosActuales.length === 0) { div.classList.add('hidden'); return; }
    div.classList.remove('hidden');
    div.innerHTML = serviciosActuales.map(s => `<span class="inline-flex items-center gap-1 px-2 py-1 bg-zinc-800 border border-zinc-700 text-zinc-200 text-xs rounded-sm">${s} <button type="button" onclick="quitarServicio('${s}')" class="text-zinc-500 hover:text-red-400">×</button></span>`).join('');
}

window.quitarServicio = function(s) {
    serviciosActuales = serviciosActuales.filter(x => x !== s);
    actualizarUISeleccion();
}
"""
    js = js.replace("if(document.getElementById('registro-form'))", servicios_actuales + "\nif(document.getElementById('registro-form'))")
    print("Injected serviciosActuales and multi-select")

open('app.js', 'w', encoding='utf-8').write(js)
print("\n✅ All missing functions injected into app.js")

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("Cache busted")
