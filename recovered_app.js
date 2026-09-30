// Estado Global
let registros = [];
let pagosNomina = [];
let sucursalesActivas = ['La Morena', 'La Quemada', 'Nativitas'];
let barberosActivos = ['David', 'Brandon', 'Mario', 'Gabo', 'Carlos'];
let serviciosActivos = ['Corte', 'Corte y Barba', 'Barba', 'Express', 'Otro'];
let bebidasActivas = ['-', 'Agua', 'Coca Cola', 'Cerveza', 'Jugo'];

let sucursalActual = 'La Morena';
let rolActual = null;

const formatoDinero = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' });

// ==========================================
// 1. SISTEMA DE ROLES Y PIN
// ==========================================
let rolPendiente = null;

function renderizarBotonesLogin() {
    const container = document.getElementById('login-roles');
    container.innerHTML = `
        <button onclick="promptPin('admin')" class="w-full bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-4 px-6 rounded-xl transition-transform hover:scale-105 flex items-center justify-center gap-3 shadow-lg">
            <i class="fa-solid fa-user-tie text-xl"></i> Acceso Dueño / Admin
        </button>
        <div class="h-px bg-gray-700 my-6"></div>
    `;
    [...sucursalesActivas].sort().forEach(suc => {
        container.innerHTML += `
            <button onclick="promptPin('caja_${suc}')" class="w-full bg-white hover:bg-gray-200 text-black font-bold py-3 px-6 rounded-xl transition-transform hover:scale-105 flex justify-between items-center shadow-lg mb-4">
                <span><i class="fa-solid fa-desktop text-gray-500 mr-2"></i> Tienda ${suc}</span><i class="fa-solid fa-chevron-right text-gray-400"></i>
            </button>
        `;
    });
}

function promptPin(rol) {
    rolPendiente = rol;
    document.getElementById('login-roles').classList.add('hidden');
    document.getElementById('login-pin').classList.remove('hidden');
    document.getElementById('pin-error').classList.add('hidden');
    const input = document.getElementById('pin-input');
    input.value = '';
    setTimeout(() => input.focus(), 100);
}
function cancelarPin() {
    rolPendiente = null;
    document.getElementById('login-roles').classList.remove('hidden');
    document.getElementById('login-pin').classList.add('hidden');
}
function verificarPin() {
    const input = document.getElementById('pin-input').value;
    if(input === '9999') {
        iniciarSesion(rolPendiente); cancelarPin(); 
    } else {
        document.getElementById('pin-error').classList.remove('hidden');
        document.getElementById('pin-input').value = '';
    }
}
function iniciarSesion(rol) {
    rolActual = rol;
    document.getElementById('pantalla-login').classList.add('hidden');
    document.getElementById('main-app').classList.remove('hidden');
    
    const tabs = document.getElementById('contenedor-tabs');
    const selectorSuc = document.getElementById('contenedor-sucursal');
    const btnConfig = document.getElementById('btn-config');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const etiquetaRol = document.getElementById('etiqueta-rol');
    const textoRol = document.getElementById('texto-rol');
    const labelBitacora = document.getElementById('label-bitacora-sucursal');
    const panelComisiones = document.getElementById('panel-comisiones');

    tabs.classList.add('hidden'); selectorSuc.classList.add('hidden'); btnConfig.classList.add('hidden');
    btnLimpiar.classList.add('hidden'); etiquetaRol.classList.remove('hidden'); panelComisiones.classList.add('hidden');
    
    if(rol === 'admin') {
        tabs.classList.remove('hidden'); selectorSuc.classList.remove('hidden'); btnConfig.classList.remove('hidden');
        btnLimpiar.classList.remove('hidden'); etiquetaRol.classList.add('hidden'); panelComisiones.classList.remove('hidden');
        labelBitacora.textContent = '(Todas)';
        
        const selSucursal = document.getElementById('sucursal-select');
        selSucursal.innerHTML = '';
        [...sucursalesActivas].sort().forEach(s => selSucursal.innerHTML += `<option value="${s}" class="text-black">Sucursal: ${s}</option>`);
        sucursalActual = selSucursal.value;
    } else {
        sucursalActual = rol.replace('caja_', '');
        textoRol.textContent = 'Tienda: ' + sucursalActual;
        document.getElementById('label-sucursal-form').textContent = sucursalActual;
        labelBitacora.textContent = `(Solo ${sucursalActual})`;
    }
    
    const hoyLocal = new Date();
    const tOffset = hoyLocal.getTimezoneOffset() * 60000;
    const hoyIso = new Date(hoyLocal - tOffset).toISOString().split('T')[0];
    document.getElementById('filtro-fecha-pos').value = hoyIso;
    
    actualizarVistaHoy();
}
function cerrarSesion() {
    rolActual = null;
    document.getElementById('pantalla-login').classList.remove('hidden');
    document.getElementById('main-app').classList.add('hidden');
    document.getElementById('tab-pos').click();
}

// ==========================================
// 2. MODAL CUSTOM DE CONFIRMACIÓN
// ==========================================
let confirmCallback = null;
const modalConfirm = document.getElementById('modal-confirm');
function mostrarConfirmacion(titulo, mensaje, onConfirm) {
    document.getElementById('confirm-title').textContent = titulo;
    document.getElementById('confirm-message').textContent = mensaje;
    confirmCallback = onConfirm; modalConfirm.classList.remove('hidden');
}
document.getElementById('btn-confirm-cancel').addEventListener('click', () => { modalConfirm.classList.add('hidden'); confirmCallback = null; });
document.getElementById('btn-confirm-ok').addEventListener('click', () => { modalConfirm.classList.add('hidden'); if(confirmCallback) confirmCallback(); });


// ==========================================
// 3. CONFIGURACIÓN (MODAL)
// ==========================================
const modalConfig = document.getElementById('modal-config');
document.getElementById('btn-config').addEventListener('click', () => modalConfig.classList.remove('hidden'));
document.getElementById('btn-cerrar-modal').addEventListener('click', () => modalConfig.classList.add('hidden'));

function actualizarSelectsForm() {
    const sBarbero = document.getElementById('barbero'); const sServicio = document.getElementById('servicio'); const sBebida = document.getElementById('bebida');
    sBarbero.innerHTML = '<option value="">Selecciona un barbero...</option>'; barberosActivos.sort().forEach(b => sBarbero.innerHTML += `<option value="${b}">${b}</option>`);
    sServicio.innerHTML = ''; serviciosActivos.forEach(s => sServicio.innerHTML += `<option value="${s}">${s}</option>`);
    sBebida.innerHTML = ''; bebidasActivas.forEach(b => sBebida.innerHTML += `<option value="${b}">${b}</option>`);
}
function renderizarListaModal(contenedorId, arrayOriginal, fnEliminar) {
    const container = document.getElementById(contenedorId); container.innerHTML = '';
    if(arrayOriginal.length === 0) { container.innerHTML = '<div class="p-3 text-sm text-gray-500 text-center">Vacío</div>'; return; }
    [...arrayOriginal].sort().forEach(item => {
        container.innerHTML += `
            <div class="flex justify-between items-center p-3 border-b border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-800 last:border-0">
                <span class="font-medium text-gray-700 dark:text-gray-200">${item}</span>
                <button onclick="${fnEliminar}('${item}')" class="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50 dark:hover:bg-red-900/30"><i class="fa-solid fa-trash-alt text-sm"></i></button>
            </div>`;
    });
}
function actualizarTodasLasListas() {
    renderizarListaModal('lista-sucursales-modal', sucursalesActivas, 'eliminarSucursal');
    renderizarListaModal('lista-barberos-modal', barberosActivos, 'eliminarBarbero');
    renderizarListaModal('lista-servicios-modal', serviciosActivos, 'eliminarServicio');
    renderizarListaModal('lista-bebidas-modal', bebidasActivas, 'eliminarBebida');
    actualizarSelectsForm();
    renderizarBotonesLogin();
}

function eliminarSucursal(n) { mostrarConfirmacion('Eliminar Sucursal', `¿Eliminar ${n}?`, () => { sucursalesActivas = sucursalesActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarBarbero(n) { mostrarConfirmacion('Eliminar Barbero', `¿Eliminar a ${n}?`, () => { barberosActivos = barberosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarServicio(n) { mostrarConfirmacion('Eliminar Servicio', `¿Eliminar ${n}?`, () => { serviciosActivos = serviciosActivos.filter(b => b !== n); actualizarTodasLasListas(); }); }
function eliminarBebida(n) { mostrarConfirmacion('Eliminar Bebida', `¿Eliminar ${n}?`, () => { bebidasActivas = bebidasActivas.filter(b => b !== n); actualizarTodasLasListas(); }); }

document.getElementById('form-nueva-sucursal').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-sucursal-nombre').value.trim(); if(v && !sucursalesActivas.includes(v)) { sucursalesActivas.push(v); document.getElementById('nueva-sucursal-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-barbero').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-barbero-nombre').value.trim(); if(v && !barberosActivos.includes(v)) { barberosActivos.push(v); document.getElementById('nuevo-barbero-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nuevo-servicio').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nuevo-servicio-nombre').value.trim(); if(v && !serviciosActivos.includes(v)) { serviciosActivos.push(v); document.getElementById('nuevo-servicio-nombre').value=''; actualizarTodasLasListas(); }});
document.getElementById('form-nueva-bebida').addEventListener('submit', (e) => { e.preventDefault(); const v = document.getElementById('nueva-bebida-nombre').value.trim(); if(v && !bebidasActivas.includes(v)) { bebidasActivas.push(v); document.getElementById('nueva-bebida-nombre').value=''; actualizarTodasLasListas(); }});


// ==========================================
// 4. CORE: PUNTO DE VENTA (HOY/FECHA SELECCIONADA)
// ==========================================
document.getElementById('sucursal-select').addEventListener('change', (e) => {
    sucursalActual = e.target.value; document.getElementById('label-sucursal-form').textContent = sucursalActual; actualizarVistaHoy();
});
document.getElementById('filtro-fecha-pos').addEventListener('change', actualizarVistaHoy);

function toggleMixto(isMixto) {
    const panel = document.getElementById('panel-mixto');
    if(isMixto) { panel.classList.remove('hidden'); calcularRestanteMixto(); } else { panel.classList.add('hidden'); }
}
document.getElementById('monto').addEventListener('input', calcularRestanteMixto);
document.getElementById('propina').addEventListener('input', calcularRestanteMixto);

function calcularRestanteMixto() {
    if(document.getElementById('panel-mixto').classList.contains('hidden')) return;
    const totalACobrar = (parseFloat(document.getElementById('monto').value) || 0) + (parseFloat(document.getElementById('propina').value) || 0);
    document.getElementById('total-mixto-label').textContent = formatoDinero.format(totalACobrar);
    const restante = totalACobrar - (parseFloat(document.getElementById('monto-efectivo-mixto').value) || 0);
    document.getElementById('restante-tarjeta-label').textContent = formatoDinero.format(restante < 0 ? 0 : restante);
}

document.getElementById('registro-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const fechaFiltro = document.getElementById('filtro-fecha-pos').value;
    const fechaElegida = new Date(fechaFiltro + 'T12:00:00'); 
    
    const now = new Date(); 
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const propina = parseFloat(document.getElementById('propina').value) || 0;
    const totalCobrado = monto + propina;
    let tipoPago = document.querySelector('input[name="pago"]:checked').value;
    let valEfectivo = 0, valTarjeta = 0;
    
    if(tipoPago === 'Efectivo') valEfectivo = totalCobrado;
    else if(tipoPago === 'Tarjeta') valTarjeta = totalCobrado;
    else {
        valEfectivo = parseFloat(document.getElementById('monto-efectivo-mixto').value) || 0;
        valTarjeta = totalCobrado - valEfectivo; if(valTarjeta < 0) valTarjeta = 0;
    }
    
    registros.unshift({
        id: Date.now(), fechaObj: fechaElegida, fechaCorta: fechaFiltro,
        hora: now.toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'}),
        sucursal: sucursalActual, barbero: document.getElementById('barbero').value,
        servicio: document.getElementById('servicio').value, bebida: document.getElementById('bebida').value,
        monto, propina, pagoTxt: tipoPago, valEfectivo, valTarjeta
    });
    
    document.getElementById('barbero').value = ''; document.getElementById('propina').value = '0'; document.getElementById('monto').value = '220';
    if(tipoPago === 'Mixto') { document.getElementById('monto-efectivo-mixto').value = '0'; calcularRestanteMixto(); }
    actualizarVistaHoy();
});

function actualizarVistaHoy() {
    const fechaFiltro = document.getElementById('filtro-fecha-pos').value;
    
    let registrosHoy = registros.filter(r => r.fechaCorta === fechaFiltro);
    if(rolActual !== 'admin') registrosHoy = registrosHoy.filter(r => r.sucursal === sucursalActual);
    
    const tbody = document.getElementById('tabla-registros'); tbody.innerHTML = '';
    const colHeaderAccion = document.querySelector('.col-accion');
    if(rolActual === 'admin') { if(colHeaderAccion) colHeaderAccion.classList.remove('hidden'); } else { if(colHeaderAccion) colHeaderAccion.classList.add('hidden'); }
    
    if(registrosHoy.length === 0) { tbody.innerHTML = `<tr><td colspan="8" class="p-6 text-center text-gray-500">No hay registros para este día.</td></tr>`; }
    
    let tIngresos = 0, tEfectivo = 0, tTarjeta = 0; const res = {};
    
    registrosHoy.sort((a,b) => b.id - a.id).forEach((reg, index) => {
        tIngresos += reg.monto; tEfectivo += reg.valEfectivo; tTarjeta += reg.valTarjeta;
        if(!res[reg.barbero]) res[reg.barbero] = { cortes: 0, comision: 0, propinas: 0 };
        res[reg.barbero].cortes++; res[reg.barbero].comision += (reg.monto * 0.5); res[reg.barbero].propinas += reg.propina;

        const row = document.createElement('tr');
        if(index === 0) row.className = 'new-row dark:bg-yellow-900/20';
        
        let cSuc = 'text-gray-600 dark:text-gray-400';
        // Generar un color semi-aleatorio predecible basado en el string para cualquier sucursal nueva
        let badgeStyle = '';
        if(reg.sucursal === 'La Morena') badgeStyle = 'text-yellow-600 dark:text-yellow-400 border-yellow-200 dark:border-yellow-800/50';
        else if(reg.sucursal === 'La Quemada') badgeStyle = 'text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800/50';
        else if(reg.sucursal === 'Nativitas') badgeStyle = 'text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800/50';
        else badgeStyle = 'text-pink-600 dark:text-pink-400 border-pink-200 dark:border-pink-800/50';
        
        let bPago = '';
        if(reg.pagoTxt === 'Efectivo') bPago = `<span class="px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">Efectivo</span>`;
        else if(reg.pagoTxt === 'Tarjeta') bPago = `<span class="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">Tarjeta</span>`;
        else bPago = `<span class="px-2 py-1 rounded text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300" title="Ef: ${formatoDinero.format(reg.valEfectivo)} | Tarj: ${formatoDinero.format(reg.valTarjeta)}">Mixto</span>`;

        let btnEl = rolActual === 'admin' ? `<td class="p-3 text-right"><button onclick="eliminarRegistro(${reg.id})" class="text-red-500 hover:text-red-700 dark:text-red-400"><i class="fa-solid fa-times"></i></button></td>` : '';
        row.innerHTML = `<td class="p-3"><span class="text-xs font-bold ${badgeStyle} border px-2 py-1 rounded bg-white dark:bg-gray-800">${reg.sucursal}</span></td>
            <td class="p-3 text-gray-500 dark:text-gray-400">${reg.hora}</td><td class="p-3 font-medium dark:text-white">${reg.barbero}</td><td class="p-3 dark:text-gray-200">${reg.servicio}</td>
            <td class="p-3 dark:text-gray-200">${formatoDinero.format(reg.monto)}</td><td class="p-3 text-green-600 dark:text-green-400">${reg.propina > 0 ? '+'+formatoDinero.format(reg.propina) : '-'}</td><td class="p-3">${bPago}</td>${btnEl}`;
        tbody.appendChild(row);
    });
    
    document.getElementById('total-ingresos').textContent = formatoDinero.format(tIngresos); document.getElementById('total-efectivo').textContent = formatoDinero.format(tEfectivo);
    document.getElementById('total-tarjeta').textContent = formatoDinero.format(tTarjeta); document.getElementById('total-cortes').textContent = registrosHoy.length;
    
    if(rolActual === 'admin') {
        const grid = document.getElementById('barberos-grid'); grid.innerHTML = '';
        Object.keys(res).sort().forEach(n => {
            const s = res[n];
            grid.innerHTML += `<div class="border dark:border-gray-700 rounded-lg p-3 bg-gray-50 dark:bg-gray-800/50 flex flex-col relative overflow-hidden"><div class="absolute top-0 left-0 w-1 h-full bg-yellow-500"></div>
                <div class="flex justify-between items-center mb-2 pl-2"><span class="font-bold text-gray-800 dark:text-white">${n}</span><span class="text-xs bg-gray-200 dark:bg-gray-700 dark:text-gray-200 px-2 py-1 rounded-full">${s.cortes} serv.</span></div>
                <div class="mt-auto pl-2"><p class="text-xs text-gray-500 flex justify-between">Comisión: <span>${formatoDinero.format(s.comision)}</span></p><p class="text-xs text-gray-500 flex justify-between">Propinas: <span>${formatoDinero.format(s.propinas)}</span></p>
                <div class="border-t dark:border-gray-600 mt-1 pt-1 flex justify-between font-bold"><span class="dark:text-gray-200">Total Pago:</span><span class="text-green-600 dark:text-green-400">${formatoDinero.format(s.comision + s.propinas)}</span></div></div></div>`;
        });
    }
}

function eliminarRegistro(id) {
    if(rolActual !== 'admin') return;
    mostrarConfirmacion('Eliminar Registro', '¿Seguro que deseas borrar este registro de la bitácora?', () => {
        registros = registros.filter(r => r.id !== id); actualizarVistaHoy(); if(!document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
    });
}
document.getElementById('btn-limpiar').addEventListener('click', () => {
    if(rolActual !== 'admin') return;
    const fechaFiltro = document.getElementById('filtro-fecha-pos').value;
    mostrarConfirmacion('Limpiar Registros', `¿Borrar todos los datos de ${fechaFiltro}? Esta acción no se puede deshacer.`, () => {
        registros = registros.filter(r => r.fechaCorta !== fechaFiltro);
        actualizarVistaHoy(); if(!document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
    });
});


// ==========================================
// 5. REPORTES DINÁMICOS POR PERIODO
// ==========================================
document.getElementById('tab-pos').addEventListener('click', () => {
    document.getElementById('vista-pos').classList.remove('hidden'); document.getElementById('vista-reportes').classList.add('hidden');
    document.getElementById('tab-pos').className = "py-3 px-2 border-b-2 border-yellow-500 text-yellow-600 dark:text-yellow-400 font-bold transition-colors";
    document.getElementById('tab-reportes').className = "py-3 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white font-medium transition-colors";
});
document.getElementById('tab-reportes').addEventListener('click', () => {
    document.getElementById('vista-pos').classList.add('hidden'); document.getElementById('vista-reportes').classList.remove('hidden');
    document.getElementById('tab-reportes').className = "py-3 px-2 border-b-2 border-yellow-500 text-yellow-600 dark:text-yellow-400 font-bold transition-colors";
    document.getElementById('tab-pos').className = "py-3 px-2 border-b-2 border-transparent text-gray-500 hover:text-gray-800 dark:text-gray-400 dark:hover:text-white font-medium transition-colors";
    
    if(!document.getElementById('reporte-desde').value) {
        document.getElementById('quick-date-select').value = 'este_mes';
        applyQuickDate();
    } else {
        actualizarReportes();
    }
});

function applyQuickDate() {
    const val = document.getElementById('quick-date-select').value;
    if(val === 'custom') return;
    
    const now = new Date();
    let desde = new Date(); let hasta = new Date();

    if(val === 'este_mes') {
        desde = new Date(now.getFullYear(), now.getMonth(), 1);
        hasta = new Date(now.getFullYear(), now.getMonth() + 1, 0); 
    } else if (val === 'mes_pasado') {
        desde = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        hasta = new Date(now.getFullYear(), now.getMonth(), 0);
    } else if (val === 'esta_semana') {
        const day = now.getDay() || 7; 
        desde = new Date(now); desde.setDate(now.getDate() - day + 1);
        hasta = new Date(desde); hasta.setDate(desde.getDate() + 6);
    } else if (val === 'semana_pasada') {
        const day = now.getDay() || 7;
        hasta = new Date(now); hasta.setDate(now.getDate() - day); 
        desde = new Date(hasta); desde.setDate(hasta.getDate() - 6); 
    }

    const tOff = desde.getTimezoneOffset() * 60000;
    document.getElementById('reporte-desde').value = new Date(desde - tOff).toISOString().split('T')[0];
    document.getElementById('reporte-hasta').value = new Date(hasta - tOff).toISOString().split('T')[0];
    
    actualizarReportes();
}

document.getElementById('reporte-desde').addEventListener('change', () => document.getElementById('quick-date-select').value = 'custom');
document.getElementById('reporte-hasta').addEventListener('change', () => document.getElementById('quick-date-select').value = 'custom');
document.getElementById('btn-filtrar-reportes').addEventListener('click', actualizarReportes);

document.getElementById('btn-theme').addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const icon = document.getElementById('icon-theme');
    if(document.documentElement.classList.contains('dark')) icon.classList.replace('fa-moon', 'fa-sun'); else icon.classList.replace('fa-sun', 'fa-moon');
    if(!document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
});

let chartTendenciaInst; let chartBarberosInst;

function actualizarReportes() {
    if(rolActual !== 'admin') return;
    
    const desdeStr = document.getElementById('reporte-desde').value;
    const hastaStr = document.getElementById('reporte-hasta').value;
    if(!desdeStr || !hastaStr) return;
    
    const dateDesde = new Date(desdeStr + 'T00:00:00');
    const dateHasta = new Date(hastaStr + 'T23:59:59');
    
    const regsPeriodo = registros.filter(r => r.fechaObj >= dateDesde && r.fechaObj <= dateHasta);
    const pagosPeriodo = pagosNomina.filter(p => p.fechaObj >= dateDesde && p.fechaObj <= dateHasta);
    
    const totalIngresos = regsPeriodo.reduce((sum, r) => sum + r.monto, 0);
    const totalPagos = pagosPeriodo.reduce((sum, p) => sum + p.monto, 0);

    document.getElementById('rep-ingresos-periodo').textContent = formatoDinero.format(totalIngresos);
    document.getElementById('rep-cortes-periodo').textContent = regsPeriodo.length;
    document.getElementById('rep-propina-promedio').textContent = formatoDinero.format(regsPeriodo.length > 0 ? regsPeriodo.reduce((sum, r) => sum + r.propina, 0) / regsPeriodo.length : 0);
    document.getElementById('rep-pagos-periodo').textContent = formatoDinero.format(totalPagos);

    // Gráfica de Tendencia (Agrupando por fecha en el periodo)
    const mapFechas = {};
    regsPeriodo.forEach(r => {
        if(!mapFechas[r.fechaCorta]) mapFechas[r.fechaCorta] = 0;
        mapFechas[r.fechaCorta] += r.monto;
    });
    const labelsTendencia = Object.keys(mapFechas).sort();
    const datosTendencia = labelsTendencia.map(f => mapFechas[f]);
    
    // Gráfica y Tabla de Nómina (Agrupando por Barbero en el periodo)
    const mapBarberos = {}; 
    const mapNomina = {};
    barberosActivos.forEach(b => mapNomina[b] = { generado: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        const ganancia = (r.monto * 0.5) + r.propina;
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        if(mapNomina[r.barbero]) mapNomina[r.barbero].generado += ganancia;
    });

    pagosPeriodo.forEach(p => {
        if(mapNomina[p.barbero]) mapNomina[p.barbero].pagado += p.monto;
    });
    
    const tbodyNomina = document.getElementById('tabla-nomina-barberos'); tbodyNomina.innerHTML = '';
    if(Object.keys(mapNomina).length === 0) tbodyNomina.innerHTML = `<tr><td colspan="5" class="p-6 text-center text-gray-500">No hay datos en este periodo.</td></tr>`;
    
    Object.keys(mapNomina).sort().forEach(b => {
        const stats = mapNomina[b];
        const saldo = stats.generado - stats.pagado;
        if(stats.generado === 0 && stats.pagado === 0) return;
        
        tbodyNomina.innerHTML += `
            <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="p-3 font-bold dark:text-white">${b}</td>
                <td class="p-3 text-center border-l dark:border-gray-700 text-blue-600 dark:text-blue-400">--</td>
                <td class="p-3 text-center border-l dark:border-gray-700 text-gray-600 dark:text-gray-300">${formatoDinero.format(stats.generado)}</td>
                <td class="p-3 text-center border-l dark:border-gray-700 text-gray-600 dark:text-gray-300">${formatoDinero.format(stats.pagado)}</td>
                <td class="p-3 text-right border-l dark:border-gray-700 font-bold ${saldo > 0 ? 'text-red-500' : 'text-green-500'}">${formatoDinero.format(saldo)}</td>
                <td class="p-3 text-center border-l dark:border-gray-700">
                    <button onclick="abrirModalPago('${b}', ${saldo})" class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs font-bold transition-colors" ${saldo <= 0 ? 'disabled style="opacity:0.5"' : ''}>Liquidar</button>
                </td>
            </tr>`;
    });

    const tbodyPagos = document.getElementById('tabla-historial-pagos'); tbodyPagos.innerHTML = '';
    if(pagosPeriodo.length === 0) tbodyPagos.innerHTML = `<tr><td colspan="4" class="p-6 text-center text-gray-500">No hay pagos emitidos en este periodo.</td></tr>`;
    
    [...pagosPeriodo].sort((a,b) => b.fechaObj - a.fechaObj).forEach(p => {
        tbodyPagos.innerHTML += `
            <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                <td class="p-3 text-gray-500 dark:text-gray-400">${p.fechaStr}</td>
                <td class="p-3 font-bold dark:text-white">${p.barbero}</td>
                <td class="p-3 text-green-600 dark:text-green-400 font-bold">${formatoDinero.format(p.monto)}</td>
                <td class="p-3 dark:text-gray-300"><span class="px-2 py-1 rounded text-xs font-medium bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300">${p.metodo}</span></td>
            </tr>`;
    });
    
    const isDark = document.documentElement.classList.contains('dark');
    const cT = isDark ? '#9ca3af' : '#4b5563'; const cG = isDark ? '#374151' : '#e5e7eb'; 
    if(chartTendenciaInst) chartTendenciaInst.destroy();
    chartTendenciaInst = new Chart(document.getElementById('chartTendencia').getContext('2d'), { type: 'line', data: { labels: labelsTendencia, datasets: [{ data: datosTendencia, borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', borderWidth: 3, tension: 0.4, fill: true }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: cG }, ticks: { color: cT } }, x: { grid: { display: false }, ticks: { color: cT } } } } });
    if(chartBarberosInst) chartBarberosInst.destroy();
    chartBarberosInst = new Chart(document.getElementById('chartBarberos').getContext('2d'), { type: 'bar', data: { labels: Object.keys(mapBarberos), datasets: [{ data: Object.values(mapBarberos), backgroundColor: '#eab308', borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: cG }, ticks: { color: cT } }, x: { grid: { display: false }, ticks: { color: cT } } } } });
}


// ==========================================
// 6. LÓGICA DE PAGOS A BARBEROS
// ==========================================
const modalPago = document.getElementById('modal-pago');
function abrirModalPago(barbero, saldoPendiente) {
    document.getElementById('pago-barbero-nombre').value = barbero;
    document.getElementById('pago-monto').value = saldoPendiente; 
    modalPago.classList.remove('hidden');
}
function cerrarModalPago() { modalPago.classList.add('hidden'); }

document.getElementById('form-pago-barbero').addEventListener('submit', (e) => {
    e.preventDefault(); const now = new Date();
    const barbero = document.getElementById('pago-barbero-nombre').value;
    const monto = parseFloat(document.getElementById('pago-monto').value);
    const metodo = document.getElementById('pago-metodo').value;
    
    const hastaStr = document.getElementById('reporte-hasta').value || now.toISOString().split('T')[0];
    const fechaPago = new Date(hastaStr + 'T12:00:00'); 
    
    pagosNomina.unshift({
        id: Date.now(), fechaObj: fechaPago,
        fechaStr: fechaPago.toLocaleString('es-MX', {day:'2-digit', month:'2-digit', year:'numeric'}),
        barbero, monto, metodo
    });
    
    cerrarModalPago(); actualizarReportes();
});


// ==========================================
// 7. INICIALIZACIÓN CON DATOS DUMMY
// ==========================================
function generarDatosHistoricos() {
    for(let i=0; i<300; i++) {
        const d = new Date(); d.setDate(d.getDate() - Math.floor(Math.random() * 60)); 
        const propina = Math.random() > 0.5 ? 20 : 0; const monto = 220;
        const tipoPago = Math.random() > 0.6 ? 'Tarjeta' : (Math.random() > 0.2 ? 'Efectivo' : 'Mixto');
        let valEf = 0, valTar = 0;
        if(tipoPago === 'Efectivo') valEf = monto + propina; else if(tipoPago === 'Tarjeta') valTar = monto + propina; else { valEf = 100; valTar = (monto + propina) - 100; }
        registros.push({
            id: Date.now() + i, fechaObj: d, fechaCorta: d.toISOString().split('T')[0], hora: d.toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'}),
            sucursal: ['La Morena', 'La Quemada', 'Nativitas'][Math.floor(Math.random()*3)], barbero: barberosActivos[Math.floor(Math.random() * barberosActivos.length)],
            servicio: 'Corte', bebida: '-', monto, propina, pagoTxt: tipoPago, valEfectivo: valEf, valTarjeta: valTar
        });
    }
    registros.sort((a,b) => b.fechaObj - a.fechaObj);
    
    const now = new Date();
    const ayer = new Date(); ayer.setDate(ayer.getDate() - 1);
    const hace7 = new Date(); hace7.setDate(hace7.getDate() - 7);
    
    pagosNomina.push({ id: 1, fechaObj: ayer, fechaStr: ayer.toLocaleString('es-MX', {day:'2-digit', month:'2-digit', year:'numeric'}), barbero: 'David', monto: 1500, metodo: 'Transferencia' });
    pagosNomina.push({ id: 2, fechaObj: hace7, fechaStr: hace7.toLocaleString('es-MX', {day:'2-digit', month:'2-digit', year:'numeric'}), barbero: 'Mario', monto: 800, metodo: 'Efectivo' });
}

generarDatosHistoricos();
actualizarTodasLasListas();
renderizarBotonesLogin();