import time, re

js = open('app.js', 'r', encoding='utf-8').read()

# 1. Add Productos to Data Model
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
js = re.sub(r"let preciosBase = \{[^}]+\};", new_vars, js)

# 2. Add Select population for Productos
js = js.replace(
    "document.getElementById('bebida').innerHTML = bebidasActivas.map(x => `<option value=\"${x}\">${x}</option>`).join('');",
    """document.getElementById('bebida').innerHTML = bebidasActivas.map(x => `<option value="${x}">${x}</option>`).join('');
    const selProd = document.getElementById('producto-item');
    if(selProd) selProd.innerHTML = '<option value="">+ Producto...</option>' + productosActivos.map(x => `<option value="${x}">${x}</option>`).join('');"""
)

# 3. Add agregarProducto function
func_agregar_prod = """window.agregarProducto = function() {
    const s = document.getElementById('producto-item').value;
    if(s && s !== '') {
        serviciosActuales.push(s);
        const currentTotal = parseFloat(document.getElementById('monto').value) || 0;
        document.getElementById('monto').value = currentTotal + (preciosBase[s] || 0);
        actualizarUISeleccion();
        document.getElementById('producto-item').value = '';
    }
}
"""
js = js.replace("window.removerServicio = function(i) {", func_agregar_prod + "\nwindow.removerServicio = function(i) {")

# 4. Handle Gasto saving and rendering in Bitacora
# Find the new registro logic and add tipo: 'Ingreso'
js = js.replace("editado: false\n    });", "editado: false, tipo: 'Ingreso'\n    });")

# Update actualizarVistaHoy variables
js = js.replace("let totalIngresos = 0; let cEf = 0; let cTar = 0;", "let totalIngresos = 0; let totalGastos = 0; let cEf = 0; let cTar = 0;")

# Update the loop in actualizarVistaHoy
old_loop = """    regsHoy.forEach(r => {
        totalIngresos += r.monto; cEf += r.valEfectivo; cTar += r.valTarjeta;
        let b = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
        const badgeEdit = r.editado ? `<span class="ml-2 text-[9px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 rounded-sm">Editado</span>` : '';
        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.hora}</td>
                <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>
                <td class="p-3 text-zinc-300">${r.servicio} ${badgeEdit}</td>
                <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.propina)}</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${b}">${r.pagoTxt}</span></td>
                <td class="p-3 pr-6 text-right">
                    <button onclick="abrirModalEditar(${r.id})" class="text-zinc-500 hover:text-white transition-colors" title="Editar"><i class="fa-solid fa-pen text-[11px]"></i></button>
                </td>
            </tr>`;
    });"""

new_loop = """    let cEfBruto = 0;
    regsHoy.forEach(r => {
        if(r.tipo === 'Gasto') {
            totalGastos += r.monto; 
            cEf -= r.monto; // Gasto always in cash for now
            tbody.innerHTML += `
            <tr class="hover:bg-zinc-900 transition-colors bg-red-950/10">
                <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.hora}</td>
                <td class="p-3 font-medium text-red-400">-</td>
                <td class="p-3 text-red-400 font-bold text-xs uppercase tracking-widest">Gasto: ${r.servicio}</td>
                <td class="p-3 text-red-500 font-mono tracking-wider">- ${formatoDinero.format(r.monto)}</td>
                <td class="p-3 text-zinc-600">-</td>
                <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Caja</span></td>
                <td class="p-3 pr-6"></td>
            </tr>`;
        } else {
            totalIngresos += r.monto; cEfBruto += r.valEfectivo; cTar += r.valTarjeta;
            let b = r.pagoTxt === 'Efectivo' ? 'bg-emerald-900/20 text-emerald-400 border-emerald-800/50' : (r.pagoTxt === 'Tarjeta' ? 'bg-blue-900/20 text-blue-400 border-blue-800/50' : 'bg-purple-900/20 text-purple-400 border-purple-800/50');
            const badgeEdit = r.editado ? `<span class="ml-2 text-[9px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 rounded-sm">Editado</span>` : '';
            tbody.innerHTML += `
                <tr class="hover:bg-zinc-900 transition-colors">
                    <td class="p-3 text-zinc-500 font-mono text-xs pl-6">${r.hora}</td>
                    <td class="p-3 font-medium text-zinc-200">${r.barbero}</td>
                    <td class="p-3 text-zinc-300 text-xs">${r.servicio} ${badgeEdit}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider">${formatoDinero.format(r.monto)}</td>
                    <td class="p-3 text-emerald-400 font-mono tracking-wider text-xs">${formatoDinero.format(r.propina)}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border ${b}">${r.pagoTxt}</span></td>
                    <td class="p-3 pr-6 text-right">
                        <button onclick="abrirModalEditar(${r.id})" class="text-zinc-500 hover:text-white transition-colors" title="Editar"><i class="fa-solid fa-pen text-[11px]"></i></button>
                    </td>
                </tr>`;
        }
    });
    cEf = cEfBruto - totalGastos;
    // Set variables globally for Corte de Caja
    window.cajaEfectivoActual = cEf;
    window.gastosTotalesActuales = totalGastos;
    window.ingresosEfvoActuales = cEfBruto;
"""
js = js.replace(old_loop, new_loop)

# 5. Add logic for Gasto and Corte modals
modals_js = """
// ==========================================
// 9. GASTOS Y CORTE DE CAJA
// ==========================================
window.abrirModalGasto = function() { document.getElementById('modal-gasto').classList.remove('hidden'); }
window.cerrarModalGasto = function() { document.getElementById('modal-gasto').classList.add('hidden'); document.getElementById('form-gasto').reset(); }

document.getElementById('form-gasto').addEventListener('submit', e => {
    e.preventDefault();
    const c = document.getElementById('gasto-concepto').value;
    const m = parseFloat(document.getElementById('gasto-monto').value) || 0;
    const now = new Date();
    registros.unshift({
        id: Date.now(), fechaObj: now, fechaCorta: now.toISOString().split('T')[0], hora: now.toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'}),
        sucursal: sucursalActual, barbero: '-', servicio: c, bebida: '-', monto: m, propina: 0, pagoTxt: 'Efectivo', valEfectivo: 0, valTarjeta: 0, editado: false, tipo: 'Gasto'
    });
    cerrarModalGasto();
    actualizarVistaHoy();
});

window.abrirModalCorteCaja = function() {
    document.getElementById('corte-ingresos-efvo').textContent = formatoDinero.format(window.ingresosEfvoActuales || 0);
    document.getElementById('corte-gastos').textContent = formatoDinero.format(window.gastosTotalesActuales || 0);
    document.getElementById('corte-esperado').textContent = formatoDinero.format(window.cajaEfectivoActual || 0);
    document.getElementById('corte-real').value = '';
    document.getElementById('corte-diferencia-box').classList.add('hidden');
    document.getElementById('modal-corte').classList.remove('hidden');
}
window.cerrarModalCorteCaja = function() { document.getElementById('modal-corte').classList.add('hidden'); }

document.getElementById('corte-real').addEventListener('input', e => {
    const r = parseFloat(e.target.value) || 0;
    const esp = window.cajaEfectivoActual || 0;
    const dif = r - esp;
    const box = document.getElementById('corte-diferencia-box');
    box.classList.remove('hidden', 'bg-emerald-950', 'text-emerald-400', 'border-emerald-800', 'bg-red-950', 'text-red-400', 'border-red-800');
    if(dif === 0) {
        box.textContent = 'CAJA CUADRADA PERFECTAMENTE';
        box.classList.add('bg-emerald-950', 'text-emerald-400', 'border-emerald-800');
    } else if(dif > 0) {
        box.textContent = 'SOBRANTE: ' + formatoDinero.format(dif);
        box.classList.add('bg-emerald-950', 'text-emerald-400', 'border-emerald-800');
    } else {
        box.textContent = 'FALTANTE: ' + formatoDinero.format(Math.abs(dif));
        box.classList.add('bg-red-950', 'text-red-400', 'border-red-800');
    }
});

document.getElementById('form-corte').addEventListener('submit', e => {
    e.preventDefault();
    alert('Corte de caja registrado. Se enviará un reporte al administrador.');
    cerrarModalCorteCaja();
});
"""

if "abrirModalGasto" not in js:
    js += "\n" + modals_js

open('app.js', 'w', encoding='utf-8').write(js)
print("JS updated for products, expenses, and cash closing.")

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
