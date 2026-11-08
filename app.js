// ==========================================
// ESTADO GLOBAL
// ==========================================
let registros = JSON.parse(localStorage.getItem('mb_registros')) || [];
let pagosNomina = JSON.parse(localStorage.getItem('mb_pagos')) || [];
let historialEdiciones = JSON.parse(localStorage.getItem('mb_ediciones')) || [];
let inventarioProductos = JSON.parse(localStorage.getItem('mb_inventario')) || [
    { id: 1, nombre: 'Pomada Mate', precio: 250, stock: { 'La Morena': 15, 'La Quemada': 10, 'Nativitas': 8 }, stockMinimo: 3 },
    { id: 2, nombre: 'Pomada Brillo', precio: 250, stock: { 'La Morena': 12, 'La Quemada': 8, 'Nativitas': 6 }, stockMinimo: 3 },
    { id: 3, nombre: 'Polvo Texturizador', precio: 180, stock: { 'La Morena': 10, 'La Quemada': 6, 'Nativitas': 5 }, stockMinimo: 2 },
    { id: 4, nombre: 'Minoxidil', precio: 350, stock: { 'La Morena': 8, 'La Quemada': 5, 'Nativitas': 4 }, stockMinimo: 2 },
    { id: 5, nombre: 'Aceite para Barba', precio: 150, stock: { 'La Morena': 14, 'La Quemada': 9, 'Nativitas': 7 }, stockMinimo: 3 }
];
let metaSellos = parseInt(localStorage.getItem('mb_meta_sellos')) || 5;
let clientesLealtad = JSON.parse(localStorage.getItem('mb_clientes')) || [
    { telefono: '5512345678', nombre: 'Alejandro Ruiz', visitas: 4, sellos: 4, clienteDesde: '2026-08-15', ultimaVisita: '2026-11-01', sucursal: 'La Morena', historial: [] },
    { telefono: '5587654321', nombre: 'Roberto Gómez', visitas: 5, sellos: 5, clienteDesde: '2026-06-20', ultimaVisita: '2026-11-05', sucursal: 'La Morena', historial: [] },
    { telefono: '5544332211', nombre: 'Daniel Morales', visitas: 2, sellos: 2, clienteDesde: '2026-10-12', ultimaVisita: '2026-11-07', sucursal: 'La Quemada', historial: [] }
];
// Asegurar que todos los clientes tengan fecha de inicio/registro
clientesLealtad.forEach(c => {
    if(!c.clienteDesde) c.clienteDesde = c.fechaRegistro || c.ultimaVisita || '2026-11-01';
});
let sucursalesActivas = ['La Morena', 'La Quemada', 'Nativitas'];

window.guardarDatos = function() {
    localStorage.setItem('mb_registros', JSON.stringify(registros));
    localStorage.setItem('mb_pagos', JSON.stringify(pagosNomina));
    localStorage.setItem('mb_ediciones', JSON.stringify(historialEdiciones));
    localStorage.setItem('mb_inventario', JSON.stringify(inventarioProductos));
    localStorage.setItem('mb_clientes', JSON.stringify(clientesLealtad));
    localStorage.setItem('mb_meta_sellos', metaSellos.toString());
};
let barberosActivos = [
    {nombre: 'David', sucursal: 'La Morena'},
    {nombre: 'Brandon', sucursal: 'La Morena'},
    {nombre: 'Mario', sucursal: 'La Quemada'},
    {nombre: 'Gabo', sucursal: 'Nativitas'},
    {nombre: 'Carlos', sucursal: 'La Morena'}
];
let productosActivos = ['Pomada Mate', 'Pomada Brillo', 'Polvo Texturizador', 'Minoxidil', 'Aceite para Barba'];

let catalog = [
    { cat: 'Clásicos', items: ['Corte de Cabello', 'Corte de Barba (Ritual)', 'Corte y Barba', 'Servicio Express', 'Servicio Luxury'] },
    { cat: 'Spa y Faciales', items: ['Limpieza Facial', 'Facial y Corte', 'Facial, Corte y Barba', 'Facial y Barba', 'Corte y Masaje', 'Corte, Barba y Masaje', 'Corte y Reflexoterapia', 'Corte, Barba y Reflexoterapia'] },
    { cat: 'Extras', items: ['Tinte de Barba', 'Grecas', 'Perfilado de Cejas', 'Planchado de Cejas'] }
];
let preciosBase = {
    'Corte de Cabello': 220, 'Corte de Barba (Ritual)': 220, 'Corte y Barba': 380, 'Servicio Express': 120, 'Servicio Luxury': 550,
    'Limpieza Facial': 180, 'Facial y Corte': 330, 'Facial, Corte y Barba': 480, 'Facial y Barba': 330,
    'Corte y Masaje': 600, 'Corte, Barba y Masaje': 750, 'Corte y Reflexoterapia': 580, 'Corte, Barba y Reflexoterapia': 730,
    'Tinte de Barba': 120, 'Grecas': 80, 'Perfilado de Cejas': 80, 'Planchado de Cejas': 150,
    'Pomada Mate': 250, 'Pomada Brillo': 250, 'Polvo Texturizador': 180, 'Minoxidil': 350, 'Aceite para Barba': 150
};
let serviciosActivos = ['Corte de Cabello', 'Corte de Barba (Ritual)', 'Corte y Barba', 'Servicio Express', 'Servicio Luxury',
    'Limpieza Facial', 'Facial y Corte', 'Facial, Corte y Barba', 'Facial y Barba',
    'Corte y Masaje', 'Corte, Barba y Masaje', 'Corte y Reflexoterapia', 'Corte, Barba y Reflexoterapia',
    'Tinte de Barba', 'Grecas', 'Perfilado de Cejas', 'Planchado de Cejas'];
let bebidasActivas = ['-', 'Agua', 'Coca Cola', 'Cerveza', 'Jugo'];

let sucursalActual = 'La Morena';
let rolActual = null;
const formatoDinero = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' });
let chartTendenciaInst = null;
let chartBarberosInst = null;
let serviciosActuales = [];
let editServiciosActuales = [];
let ticketEnEdicion = null;

// ==========================================
// 1. SISTEMA DE ROLES Y PIN
// ==========================================
let rolPendiente = null;

function renderizarBotonesLogin() {
    const container = document.getElementById('login-roles');
    if(!container) return;
    container.innerHTML = `
        <button onclick="promptPin('admin')" class="w-full bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-4 px-6 rounded-xl transition-transform hover:scale-105 flex items-center justify-center gap-3 shadow-lg">
            <i class="fa-solid fa-user-tie text-xl"></i> Acceso Dueño / Admin
        </button>
        <div class="h-px bg-zinc-800 my-4"></div>
    `;
    [...sucursalesActivas].sort().forEach(suc => {
        container.innerHTML += `
            <button onclick="promptPin('caja_${suc}')" class="w-full bg-zinc-900 hover:bg-zinc-800 text-zinc-200 font-bold py-3 px-6 rounded-xl transition-transform hover:scale-105 flex justify-between items-center border border-zinc-700 mb-3">
                <span><i class="fa-solid fa-desktop text-zinc-500 mr-2"></i> Tienda ${suc}</span>
                <i class="fa-solid fa-chevron-right text-zinc-500"></i>
            </button>
        `;
    });
}

function promptPin(rol) {
    rolPendiente = rol;
    const loginRoles = document.getElementById('login-roles');
    const loginPin = document.getElementById('login-pin');
    const tituloPin = document.getElementById('titulo-login-pin');
    if(tituloPin) {
        if(rol === 'admin') tituloPin.textContent = 'PIN de Dueño / Admin';
        else tituloPin.textContent = 'PIN de ' + rol.replace('caja_', 'Tienda ');
    }
    if(loginRoles) loginRoles.classList.add('hidden');
    if(loginPin) loginPin.classList.remove('hidden');
    const pinErr = document.getElementById('pin-error');
    if(pinErr) pinErr.classList.add('hidden');
    const input = document.getElementById('pin-input');
    if(input) { input.value = ''; setTimeout(() => input.focus(), 100); }
}

function cancelarPin() {
    rolPendiente = null;
    const loginRoles = document.getElementById('login-roles');
    const loginPin = document.getElementById('login-pin');
    if(loginRoles) loginRoles.classList.remove('hidden');
    if(loginPin) loginPin.classList.add('hidden');
}

function verificarPin() {
    const input = document.getElementById('pin-input');
    if(!input) return;
    const val = input.value;
    const err = document.getElementById('pin-error');

    if(rolPendiente === 'admin') {
        // Acceso exclusivo Dueño / Admin: SOLO PIN 9999
        if(val === '9999') {
            iniciarSesion('admin');
            cancelarPin();
        } else {
            if(err) {
                err.textContent = 'Código de Dueño Incorrecto';
                err.classList.remove('hidden');
            }
            input.value = '';
        }
    } else {
        // Acceso Tiendas / Cajas: PIN de tienda '1234' o PIN maestro '9999'
        if(val === '1234' || val === '9999') {
            iniciarSesion(rolPendiente);
            cancelarPin();
        } else {
            if(err) {
                err.textContent = 'Código de Tienda Incorrecto';
                err.classList.remove('hidden');
            }
            input.value = '';
        }
    }
}

function iniciarSesion(rol) {
    rolActual = rol;
    const loginScreen = document.getElementById('pantalla-login');
    const mainApp = document.getElementById('main-app');
    if(loginScreen) loginScreen.classList.add('hidden');
    if(mainApp) { mainApp.classList.remove('hidden'); mainApp.classList.add('flex'); }

    const tabs = document.getElementById('contenedor-tabs');
    const selectorSuc = document.getElementById('contenedor-sucursal');
    const btnConfig = document.getElementById('btn-config');
    const btnLimpiar = document.getElementById('btn-limpiar');
    const etiquetaRol = document.getElementById('etiqueta-rol');
    const textoRol = document.getElementById('texto-rol');
    const labelBitacora = document.getElementById('label-bitacora-sucursal');
    const panelComisiones = document.getElementById('panel-comisiones');

    if(tabs) tabs.classList.add('hidden');
    if(selectorSuc) selectorSuc.classList.add('hidden');
    if(btnConfig) btnConfig.classList.add('hidden');
    if(btnLimpiar) btnLimpiar.classList.add('hidden');
    if(etiquetaRol) etiquetaRol.classList.remove('hidden');
    if(panelComisiones) panelComisiones.classList.add('hidden');

    if(tabs) tabs.classList.remove('hidden');
    const tabRep = document.getElementById('tab-reportes');

    if(rol === 'admin') {
        if(tabRep) { tabRep.classList.remove('hidden'); tabRep.style.display = ''; }
        if(selectorSuc) selectorSuc.classList.remove('hidden');
        if(btnConfig) btnConfig.classList.remove('hidden');
        if(btnLimpiar) btnLimpiar.classList.remove('hidden');
        if(etiquetaRol) etiquetaRol.classList.add('hidden');
        if(panelComisiones) panelComisiones.classList.remove('hidden');
        if(labelBitacora) labelBitacora.textContent = '(Todas)';

        const selSucursal = document.getElementById('sucursal-select');
        if(selSucursal) {
            selSucursal.innerHTML = '<option value="Todas" class="bg-zinc-900 text-zinc-300">Sucursal: Todas</option>';
            [...sucursalesActivas].sort().forEach(s => {
                selSucursal.innerHTML += `<option value="${s}" class="bg-zinc-900 text-zinc-300">Sucursal: ${s}</option>`;
            });
            sucursalActual = 'Todas';
        }
    } else {
        // ROL TIENDA / CAJA: NUNCA TIENE ACCESO A ADMINISTRACIÓN
        if(tabRep) { tabRep.classList.add('hidden'); tabRep.style.display = 'none'; }
        if(selectorSuc) selectorSuc.classList.add('hidden');
        if(btnConfig) btnConfig.classList.add('hidden');
        if(btnLimpiar) btnLimpiar.classList.add('hidden');
        if(panelComisiones) panelComisiones.classList.add('hidden');
        if(etiquetaRol) etiquetaRol.classList.remove('hidden');

        sucursalActual = rol.replace('caja_', '');
        if(textoRol) textoRol.textContent = 'Tienda: ' + sucursalActual;
        const labelSucForm = document.getElementById('label-sucursal-form');
        if(labelSucForm) labelSucForm.textContent = sucursalActual;
        if(labelBitacora) labelBitacora.textContent = `(Solo ${sucursalActual})`;
    }

    const hoyLocal = new Date();
    const tOffset = hoyLocal.getTimezoneOffset() * 60000;
    const hoyIso = new Date(hoyLocal - tOffset).toISOString().split('T')[0];
    const fechaInput = document.getElementById('filtro-fecha-pos');
    if(fechaInput) fechaInput.value = hoyIso;

    if(typeof cambiarTab === 'function') cambiarTab('pos');
    actualizarTodasLasListas();
    actualizarVistaHoy();
}

function cerrarSesion() {
    rolActual = null;
    const loginScreen = document.getElementById('pantalla-login');
    const mainApp = document.getElementById('main-app');
    if(loginScreen) loginScreen.classList.remove('hidden');
    if(mainApp) { mainApp.classList.add('hidden'); mainApp.classList.remove('flex'); }
    renderizarBotonesLogin();
}

// ==========================================
// 2. MODAL CONFIRMACIÓN
// ==========================================
let confirmCallback = null;
function mostrarConfirmacion(titulo, mensaje, onConfirm) {
    const modalConfirm = document.getElementById('modal-confirm');
    if(!modalConfirm) { if(confirm(mensaje)) onConfirm(); return; }
    const t = document.getElementById('confirm-title');
    const m = document.getElementById('confirm-message');
    if(t) t.textContent = titulo;
    if(m) m.textContent = mensaje;
    confirmCallback = onConfirm;
    modalConfirm.classList.remove('hidden');
}
const btnCancel = document.getElementById('btn-confirm-cancel');
const btnOk = document.getElementById('btn-confirm-ok');
if(btnCancel) btnCancel.addEventListener('click', () => { document.getElementById('modal-confirm').classList.add('hidden'); confirmCallback = null; });
if(btnOk) btnOk.addEventListener('click', () => { document.getElementById('modal-confirm').classList.add('hidden'); if(confirmCallback) confirmCallback(); });

// ==========================================
// 3. CONFIGURACION MODAL
// ==========================================
const modalConfig = document.getElementById('modal-config');
const btnCfg = document.getElementById('btn-config');
const btnCerrar = document.getElementById('btn-cerrar-modal');
if(btnCfg) btnCfg.addEventListener('click', () => { if(modalConfig) modalConfig.classList.remove('hidden'); });
if(btnCerrar) btnCerrar.addEventListener('click', () => { if(modalConfig) modalConfig.classList.add('hidden'); });

window.actualizarPrecioServicio = function(nombre, valor) {
    preciosBase[nombre] = parseFloat(valor) || 0;
};

function actualizarSelectsForm() {
    const sBarbero = document.getElementById('barbero');
    const sServicio = document.getElementById('servicio');
    const sBebida = document.getElementById('bebida');
    const eBarbero = document.getElementById('edit-barbero');
    const eServicio = document.getElementById('edit-servicio');
    const eBebida = document.getElementById('edit-bebida');
    const selProd = document.getElementById('producto-item');

    const barberosLocal = barberosActivos
        .filter(b => sucursalActual === 'Todas' || b.sucursal === sucursalActual)
        .map(b => b.nombre).sort();

    let optBarberos = '<option value="">Selecciona un barbero...</option>';
    barberosLocal.forEach(n => optBarberos += `<option value="${n}">${n}</option>`);

    let optBebidas = '<option value="-">Sin cortesía</option>';
    bebidasActivas.forEach(b => { if(b !== '-') optBebidas += `<option value="${b}">${b}</option>`; });

    let optServicios = '<option value="">Selecciona un servicio...</option>';
    catalog.forEach(grupo => {
        optServicios += `<optgroup label="${grupo.cat}">`;
        grupo.items.forEach(s => {
            if(serviciosActivos.includes(s)) optServicios += `<option value="${s}">${s} — $${preciosBase[s] || 0}</option>`;
        });
        optServicios += `</optgroup>`;
    });
    const custom = serviciosActivos.filter(s => !catalog.flatMap(g => g.items).includes(s));
    if(custom.length > 0) {
        optServicios += `<optgroup label="Otros">`;
        custom.forEach(s => optServicios += `<option value="${s}">${s} — $${preciosBase[s] || 0}</option>`);
        optServicios += `</optgroup>`;
    }

    if(sBarbero) sBarbero.innerHTML = optBarberos;
    if(eBarbero) eBarbero.innerHTML = optBarberos;
    if(sServicio) sServicio.innerHTML = optServicios;
    if(eServicio) eServicio.innerHTML = optServicios;
    if(sBebida) sBebida.innerHTML = optBebidas;
    if(eBebida) eBebida.innerHTML = optBebidas;

    if(selProd) {
        selProd.innerHTML = '<option value="">+ Añadir Producto...</option>';
        productosActivos.sort().forEach(p => {
            const prodObj = inventarioProductos.find(item => item.nombre === p);
            let stockTxt = '';
            let disabled = '';
            if (prodObj && prodObj.stock) {
                const s = sucursalActual === 'Todas' ? Object.values(prodObj.stock).reduce((a,b)=>a+b, 0) : (prodObj.stock[sucursalActual] || 0);
                if (s <= 0) {
                    stockTxt = ' — (AGOTADO)';
                    disabled = ' disabled class="text-zinc-600 bg-zinc-900"';
                } else if (s <= (prodObj.stockMinimo || 3)) {
                    stockTxt = ` — ⚠️ Quedan ${s}`;
                } else {
                    stockTxt = ` — (Stock: ${s})`;
                }
            }
            selProd.innerHTML += `<option value="${p}"${disabled}>${p} — $${preciosBase[p] || 0}${stockTxt}</option>`;
        });
    }

    actualizarSelectClientesPOS();
}

function actualizarSelectClientesPOS() {
    const sel = document.getElementById('cliente-select-existente');
    if (!sel) return;
    const currentVal = sel.value;
    sel.innerHTML = '<option value="">👤 Seleccionar cliente registrado...</option>';
    clientesLealtad.forEach(c => {
        const s = c.sellos || 0;
        const icon = s >= metaSellos ? '👑' : '⭐';
        const promo = s >= metaSellos ? ' - ¡Corte Gratis!' : '';
        const telFmt = c.telefono.replace(/(\d{2})(\d{4})(\d{4})/, '$1 $2 $3');
        sel.innerHTML += `<option value="${c.telefono}">${c.nombre} — ${telFmt} (${icon} ${s}/${metaSellos}${promo})</option>`;
    });
    if (currentVal) sel.value = currentVal;
}

window.seleccionarClienteDesdeLista = function(tel) {
    const telInput = document.getElementById('cliente-telefono');
    const nomInput = document.getElementById('cliente-nombre');
    if(!tel) {
        if(telInput) telInput.value = '';
        if(nomInput) nomInput.value = '';
        const badge = document.getElementById('badge-lealtad-cliente');
        if(badge) badge.classList.add('hidden');
        const banner = document.getElementById('banner-recompensa-lealtad');
        if(banner) banner.classList.add('hidden');
        return;
    }
    const cli = clientesLealtad.find(c => c.telefono === tel);
    if(cli) {
        if(telInput) telInput.value = cli.telefono;
        if(nomInput) nomInput.value = cli.nombre;
        buscarClienteLealtad();
    }
};

function actualizarMenuSucursalesHeader() {
    const sel = document.getElementById('sucursal-select');
    if(!sel) return;
    const current = sel.value || sucursalActual;
    sel.innerHTML = '';
    const optTodas = document.createElement('option');
    optTodas.value = 'Todas'; optTodas.textContent = 'Sucursal: Todas';
    optTodas.className = 'bg-zinc-900 text-zinc-300';
    if('Todas' === current) optTodas.selected = true;
    sel.appendChild(optTodas);
    [...sucursalesActivas].sort().forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        opt.className = 'bg-zinc-900 text-zinc-300';
        if(s === current) opt.selected = true;
        sel.appendChild(opt);
    });
}

function renderizarListaModal(contenedorId, arrayOriginal, fnEliminar) {
    const container = document.getElementById(contenedorId);
    if(!container) return;
    container.innerHTML = '';
    if(arrayOriginal.length === 0) {
        container.innerHTML = '<div class="p-4 text-xs text-zinc-600 text-center uppercase tracking-widest">Vacío</div>';
        return;
    }
    let items = [...arrayOriginal];
    if(items.length > 0 && typeof items[0] === 'object') items.sort((a,b) => a.nombre.localeCompare(b.nombre));
    else items.sort();

    items.forEach(item => {
        const isObj = typeof item === 'object';
        const val = isObj ? item.nombre : item;
        const sub = isObj ? item.sucursal : '';
        let pr = '';
        if(contenedorId === 'lista-servicios-modal' || contenedorId === 'lista-productos-modal') {
            pr = `<div class="flex items-center gap-1 mt-1 text-xs"><span class="text-emerald-500">$</span><input type="number" value="${preciosBase[val] || 0}" onchange="actualizarPrecioServicio('${val}', this.value)" class="bg-transparent text-emerald-400 font-mono w-16 focus:outline-none focus:border-b border-zinc-600 px-1"></div>`;
        } else if(sub) {
            pr = `<span class="text-[10px] text-zinc-500 tracking-widest uppercase">${sub}</span>`;
        }
        container.innerHTML += `<div class="p-3 border-b border-zinc-800 flex justify-between items-center group"><div class="flex flex-col"><span class="text-xs text-zinc-300 font-bold tracking-widest uppercase">${val}</span>${pr}</div><button type="button" onclick="${fnEliminar}('${val}')" class="text-zinc-600 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"><i class="fa-solid fa-times"></i></button></div>`;
    });
}

function actualizarTodasLasListas() {
    renderizarListaModal('lista-productos-modal', productosActivos, 'eliminarProducto');
    renderizarListaModal('lista-barberos-modal', barberosActivos, 'eliminarBarbero');
    renderizarListaModal('lista-servicios-modal', serviciosActivos, 'eliminarServicio');
    renderizarListaModal('lista-bebidas-modal', bebidasActivas, 'eliminarBebida');
    const nsuc = document.getElementById('nuevo-barbero-sucursal');
    if(nsuc) nsuc.innerHTML = sucursalesActivas.map(s => `<option value="${s}">${s}</option>`).join('');
    actualizarMenuSucursalesHeader();
    actualizarSelectsForm();
}

// Delete functions
window.eliminarProducto = function(n) { mostrarConfirmacion('Eliminar Producto', `¿Eliminar ${n}?`, () => { productosActivos = productosActivos.filter(p => p !== n); actualizarTodasLasListas(); }); };
window.eliminarBarbero = function(n) { mostrarConfirmacion('Eliminar Barbero', `¿Eliminar a ${n}?`, () => { barberosActivos = barberosActivos.filter(b => b.nombre !== n); actualizarTodasLasListas(); }); };
window.eliminarServicio = function(n) { mostrarConfirmacion('Eliminar Servicio', `¿Eliminar ${n}?`, () => { serviciosActivos = serviciosActivos.filter(s => s !== n); actualizarTodasLasListas(); }); };
window.eliminarBebida = function(n) { mostrarConfirmacion('Eliminar Bebida', `¿Eliminar ${n}?`, () => { bebidasActivas = bebidasActivas.filter(b => b !== n); actualizarTodasLasListas(); }); };

// Add forms
if(document.getElementById('form-nuevo-producto')) {
    document.getElementById('form-nuevo-producto').addEventListener('submit', e => {
        e.preventDefault();
        const v = document.getElementById('nuevo-producto-nombre').value.trim();
        const p = parseFloat(document.getElementById('nuevo-producto-precio').value) || 0;
        if(v && !productosActivos.includes(v)) {
            preciosBase[v] = p; productosActivos.push(v);
            document.getElementById('nuevo-producto-nombre').value = '';
            document.getElementById('nuevo-producto-precio').value = '';
            actualizarTodasLasListas();
        }
    });
}
if(document.getElementById('form-nuevo-barbero')) {
    document.getElementById('form-nuevo-barbero').addEventListener('submit', e => {
        e.preventDefault();
        const v = document.getElementById('nuevo-barbero-nombre').value.trim();
        const suc = document.getElementById('nuevo-barbero-sucursal') ? document.getElementById('nuevo-barbero-sucursal').value : sucursalesActivas[0];
        if(v && !barberosActivos.some(b => b.nombre === v)) {
            barberosActivos.push({nombre: v, sucursal: suc});
            document.getElementById('nuevo-barbero-nombre').value = '';
            actualizarTodasLasListas();
        }
    });
}
if(document.getElementById('form-nuevo-servicio')) {
    document.getElementById('form-nuevo-servicio').addEventListener('submit', e => {
        e.preventDefault();
        const v = document.getElementById('nuevo-servicio-nombre').value.trim();
        const pEl = document.getElementById('nuevo-servicio-precio');
        const p = parseFloat(pEl ? pEl.value : '0') || 0;
        if(v && !serviciosActivos.includes(v)) {
            preciosBase[v] = p; serviciosActivos.push(v);
            document.getElementById('nuevo-servicio-nombre').value = '';
            if(pEl) pEl.value = '';
            actualizarTodasLasListas();
        }
    });
}
if(document.getElementById('form-nueva-bebida')) {
    document.getElementById('form-nueva-bebida').addEventListener('submit', e => {
        e.preventDefault();
        const v = document.getElementById('nueva-bebida-nombre').value.trim();
        if(v && !bebidasActivas.includes(v)) {
            bebidasActivas.push(v);
            document.getElementById('nueva-bebida-nombre').value = '';
            actualizarTodasLasListas();
        }
    });
}

// ==========================================
// 4. PUNTO DE VENTA
// ==========================================
const selSuc = document.getElementById('sucursal-select');
if(selSuc) selSuc.addEventListener('change', e => {
    sucursalActual = e.target.value;
    const lbl = document.getElementById('label-sucursal-form');
    if(lbl) lbl.textContent = sucursalActual;
    actualizarVistaHoy();
    actualizarSelectsForm();
    const vistaRep = document.getElementById('vista-reportes');
    if(vistaRep && !vistaRep.classList.contains('hidden')) {
        actualizarReportes();
    }
});

const fechaInput = document.getElementById('filtro-fecha-pos');
if(fechaInput) fechaInput.addEventListener('change', actualizarVistaHoy);

// Multi-servicio
window.agregarBebida = function() {
    const sel = document.getElementById('bebida');
    if(!sel || !sel.value || sel.value === '-' || sel.value === 'Sin cortesía') return;
    const s = sel.value;
    const tag = "🍹 " + s;
    if(!serviciosActuales.includes(tag)) {
        serviciosActuales.push(tag);
        actualizarUISeleccion();
    }
    sel.value = 'Sin cortesía';
};

window.agregarServicio = function() {
    const sel = document.getElementById('servicio');
    if(!sel || !sel.value) return;
    const s = sel.value;
    if(!serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        // Auto-update monto
        const montoEl = document.getElementById('monto');
        if(montoEl) montoEl.value = (parseFloat(montoEl.value) || 0) + (preciosBase[s] || 0);
        actualizarUISeleccion();
        calcularRestanteMixto();
    }
    sel.value = '';
};

window.quitarServicio = function(s) {
    serviciosActuales = serviciosActuales.filter(x => x !== s);
    actualizarUISeleccion();
};

function actualizarUISeleccion() {
    const div = document.getElementById('servicios-seleccionados');
    if(!div) return;
    if(serviciosActuales.length === 0) { div.classList.add('hidden'); return; }
    div.classList.remove('hidden');
    div.innerHTML = serviciosActuales.map(s => `<span class="inline-flex items-center gap-1 px-2 py-1 bg-zinc-800 border border-zinc-700 text-zinc-200 text-xs rounded-sm">${s} <button type="button" onclick="quitarServicio('${s}')" class="text-zinc-500 hover:text-red-400 ml-1">×</button></span>`).join('');
}

window.agregarProducto = function() {
    const sel = document.getElementById('producto-item');
    if(!sel || !sel.value) return;
    const s = sel.value;
    if(!serviciosActuales.includes(s)) {
        serviciosActuales.push(s);
        const montoEl = document.getElementById('monto');
        if(montoEl) montoEl.value = (parseFloat(montoEl.value) || 0) + (preciosBase[s] || 0);
        actualizarUISeleccion();
        calcularRestanteMixto();
    }
    sel.value = '';
};

function toggleMixto(isMixto) {
    const panel = document.getElementById('panel-mixto');
    if(panel) { if(isMixto) { panel.classList.remove('hidden'); calcularRestanteMixto(); } else panel.classList.add('hidden'); }
}
window.toggleMixto = toggleMixto;

const montoEl = document.getElementById('monto');
const propinaEl = document.getElementById('propina');
if(montoEl) montoEl.addEventListener('input', calcularRestanteMixto);
if(propinaEl) propinaEl.addEventListener('input', calcularRestanteMixto);

function calcularRestanteMixto() {
    const panel = document.getElementById('panel-mixto');
    if(!panel || panel.classList.contains('hidden')) return;
    const total = (parseFloat(document.getElementById('monto').value) || 0) + (parseFloat(document.getElementById('propina').value) || 0);
    const lbl = document.getElementById('total-mixto-label');
    if(lbl) lbl.textContent = formatoDinero.format(total);
    const ef = parseFloat(document.getElementById('monto-efectivo-mixto')?.value) || 0;
    const rest = Math.max(0, total - ef);
    const rlbl = document.getElementById('restante-tarjeta-label');
    if(rlbl) rlbl.textContent = formatoDinero.format(rest);
}
window.calcularRestanteMixto = calcularRestanteMixto;

const regForm = document.getElementById('registro-form');
if(regForm) regForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const fechaFiltro = document.getElementById('filtro-fecha-pos').value;
    const now = new Date();
    const monto = parseFloat(document.getElementById('monto').value) || 0;
    const propina = parseFloat(document.getElementById('propina').value) || 0;
    const total = monto + propina;
    let tipoPago = document.querySelector('input[name="pago"]:checked')?.value || 'Efectivo';
    let valEfectivo = 0, valTarjeta = 0;
    if(tipoPago === 'Efectivo') valEfectivo = total;
    else if(tipoPago === 'Tarjeta') valTarjeta = total;
    else { valEfectivo = parseFloat(document.getElementById('monto-efectivo-mixto')?.value) || 0; valTarjeta = Math.max(0, total - valEfectivo); }

    
    // Si dejaron algo seleccionado pero no le dieron +, lo sumamos
    const valServ = document.getElementById('servicio')?.value;
    if (valServ && !serviciosActuales.includes(valServ)) { serviciosActuales.push(valServ); }
    const valProd = document.getElementById('producto-item')?.value;
    if (valProd && !serviciosActuales.includes(valProd)) { serviciosActuales.push(valProd); }
    const valBeb = document.getElementById('bebida')?.value;
    if (valBeb && valBeb !== '-' && valBeb !== 'Sin cortesía' && !serviciosActuales.includes("🍹 " + valBeb)) { serviciosActuales.push("🍹 " + valBeb); }

    const servicioStr = serviciosActuales.join(' + ') || 'Servicio';
    const bebida = '-';
    const barbero = document.getElementById('barbero')?.value || '';

    registros.unshift({
        id: Date.now(), fechaObj: new Date(fechaFiltro + 'T12:00:00'), fechaCorta: fechaFiltro,
        hora: now.toLocaleTimeString('es-MX', {hour: '2-digit', minute: '2-digit'}),
        sucursal: sucursalActual, barbero, servicio: servicioStr, bebida,
        monto, propina, pagoTxt: tipoPago, valEfectivo, valTarjeta, editado: false
    });

    // Descontar inventario de productos vendidos
    serviciosActuales.forEach(item => {
        const prod = inventarioProductos.find(p => p.nombre === item);
        if(prod && prod.stock) {
            const suc = sucursalActual === 'Todas' ? 'La Morena' : sucursalActual;
            prod.stock[suc] = Math.max(0, (prod.stock[suc] || 0) - 1);
        }
    });

    // Procesar Lealtad de Cliente
    const telCliente = document.getElementById('cliente-telefono')?.value?.trim() || '';
    const nomCliente = document.getElementById('cliente-nombre')?.value?.trim() || '';
    let clienteData = null;

    if (telCliente) {
        clienteData = clientesLealtad.find(c => c.telefono === telCliente);
        if (!clienteData) {
            clienteData = {
                telefono: telCliente,
                nombre: nomCliente || 'Cliente VIP',
                visitas: 1,
                sellos: 1,
                clienteDesde: fechaFiltro,
                ultimaVisita: fechaFiltro,
                sucursal: sucursalActual === 'Todas' ? 'La Morena' : sucursalActual,
                historial: []
            };
            clientesLealtad.unshift(clienteData);
        } else {
            if (nomCliente) clienteData.nombre = nomCliente;
            if (!clienteData.clienteDesde) clienteData.clienteDesde = fechaFiltro;
            clienteData.visitas = (clienteData.visitas || 0) + 1;
            if (window.recompensaLealtadAplicada) {
                clienteData.sellos = 0; // Cortesía canjeada
                window.recompensaLealtadAplicada = false;
            } else {
                clienteData.sellos = ((clienteData.sellos || 0) % metaSellos) + 1;
            }
            clienteData.ultimaVisita = fechaFiltro;
            clienteData.sucursal = sucursalActual === 'Todas' ? 'La Morena' : sucursalActual;
        }
        if(!clienteData.historial) clienteData.historial = [];
        clienteData.historial.unshift({
            fecha: fechaFiltro,
            hora: now.toLocaleTimeString('es-MX', {hour: '2-digit', minute: '2-digit'}),
            servicio: servicioStr,
            barbero,
            total
        });
    }

    // Reset
    serviciosActuales = [];
    actualizarUISeleccion();
    if(document.getElementById('barbero')) document.getElementById('barbero').value = '';
    if(document.getElementById('propina')) document.getElementById('propina').value = '0';
    if(document.getElementById('monto')) document.getElementById('monto').value = '220';
    if(document.getElementById('cliente-telefono')) document.getElementById('cliente-telefono').value = '';
    if(document.getElementById('cliente-nombre')) document.getElementById('cliente-nombre').value = '';
    if(document.getElementById('cliente-select-existente')) document.getElementById('cliente-select-existente').value = '';
    const badgeCli = document.getElementById('badge-lealtad-cliente');
    if(badgeCli) badgeCli.classList.add('hidden');
    const bannerRec = document.getElementById('banner-recompensa-lealtad');
    if(bannerRec) bannerRec.classList.add('hidden');
    if(tipoPago === 'Mixto' && document.getElementById('monto-efectivo-mixto')) document.getElementById('monto-efectivo-mixto').value = '0';
    calcularRestanteMixto();
    guardarDatos();
    actualizarVistaHoy();
    actualizarSelectsForm();

    abrirModalTicketDigital({
        barbero,
        servicio: servicioStr,
        total,
        pago: tipoPago,
        sucursal: sucursalActual === 'Todas' ? 'La Morena' : sucursalActual,
        fecha: now.toLocaleDateString('es-MX', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' }),
        cliente: clienteData
    });
});

function actualizarVistaHoy() {
    const fechaEl = document.getElementById('filtro-fecha-pos');
    if(!fechaEl) return;
    const fechaFiltro = fechaEl.value;
    let regsHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo !== 'Gasto');
    if(sucursalActual !== 'Todas') regsHoy = regsHoy.filter(r => r.sucursal === sucursalActual);
    let gastosHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo === 'Gasto');
    if(sucursalActual !== 'Todas') gastosHoy = gastosHoy.filter(r => r.sucursal === sucursalActual);

    const tbody = document.getElementById('tabla-registros');
    if(!tbody) return;
    tbody.innerHTML = '';

    if(regsHoy.length === 0 && gastosHoy.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="p-6 text-center text-zinc-600 text-[10px] uppercase tracking-widest">No hay registros para este día.</td></tr>`;
    }

    let tIngresos = 0, tEfectivo = 0, tTarjeta = 0, tPropinas = 0;
    let tPropinasEfvo = 0, tPropinasTarj = 0;
    const resBarb = {};

    // Gastos first
    gastosHoy.forEach(r => {
        tbody.innerHTML += `<tr class="hover:bg-zinc-900/50 transition-colors bg-red-950/10">
            <td class="p-3 text-zinc-600 text-[10px] uppercase tracking-widest pl-4">${r.sucursal}</td>
            <td class="p-3 text-zinc-600 font-mono text-xs">${r.hora}</td>
            <td class="p-3 text-red-400 font-bold text-xs">—</td>
            <td class="p-3 text-red-400 text-xs uppercase tracking-wider">Gasto: ${r.servicio}</td>
            <td class="p-3 text-red-500 font-mono text-xs">- ${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-zinc-600 text-xs">—</td>
            <td class="p-3"><span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-red-900/20 text-red-400 border-red-800/50">Gasto</span></td>
            <td class="p-3 text-right"><button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-red-400 transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button></td>
        </tr>`;
    });

    // Tickets
    [...regsHoy].sort((a,b) => b.id - a.id).forEach((r, i) => {
        tIngresos += r.monto; tEfectivo += r.valEfectivo; tTarjeta += r.valTarjeta; tPropinas += (r.propina || 0);
        let pEf = 0, pTar = 0;
        if(r.pagoTxt === 'Efectivo') { pEf = r.propina || 0; }
        else if(r.pagoTxt === 'Tarjeta') { pTar = r.propina || 0; }
        else {
            if((r.valTarjeta || 0) >= (r.propina || 0)) pTar = r.propina || 0;
            else { pTar = r.valTarjeta || 0; pEf = (r.propina || 0) - pTar; }
        }
        tPropinasEfvo += pEf; tPropinasTarj += pTar;
        if(!resBarb[r.barbero]) resBarb[r.barbero] = { cortes: 0, comision: 0, propinas: 0 };
        resBarb[r.barbero].cortes++;
        resBarb[r.barbero].comision += r.monto * 0.5;
        resBarb[r.barbero].propinas += (r.propina || 0);

        let bPago = '';
        if(r.pagoTxt === 'Efectivo') bPago = `<span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-emerald-900/20 text-emerald-400 border-emerald-800/50">Efectivo</span>`;
        else if(r.pagoTxt === 'Tarjeta') bPago = `<span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-blue-900/20 text-blue-400 border-blue-800/50">Tarjeta</span>`;
        else bPago = `<span class="px-2 py-0.5 rounded-sm text-[9px] uppercase tracking-widest border bg-purple-900/20 text-purple-400 border-purple-800/50">Mixto</span>`;

        const editBtn = `<button onclick="abrirModalEditar(${r.id})" class="text-zinc-600 hover:text-white transition-colors"><i class="fa-solid fa-pen text-[11px]"></i></button>`;
        const badgeEdit = r.editado ? `<span class="ml-1 text-[9px] uppercase tracking-widest text-orange-400 bg-orange-900/20 border border-orange-800/50 px-1 rounded-sm">Editado</span>` : '';
        const rowClass = i === 0 ? 'hover:bg-zinc-900 transition-colors bg-yellow-900/10' : 'hover:bg-zinc-900 transition-colors';

        let strServicio = (r.servicio || 'Servicio') + badgeEdit;
        if(r.bebida && r.bebida !== '-' && r.bebida !== 'Sin cortesía') {
            // Only add legacy bebida if it's not already in the servicio string
            if(!strServicio.includes(r.bebida)) {
                strServicio += `<div class="text-[9px] text-zinc-500 uppercase tracking-widest mt-1">🍹 Cortesía: ${r.bebida}</div>`;
            }
        }
        tbody.innerHTML += `<tr class="${rowClass}">
            <td class="p-3 text-zinc-400 text-[10px] uppercase tracking-widest pl-4 font-bold">${r.sucursal}</td>
            <td class="p-3 text-zinc-500 font-mono text-xs">${r.hora}</td>
            <td class="p-3 font-medium text-zinc-200 text-sm">${r.barbero}</td>
            <td class="p-3 text-zinc-300 text-xs">${strServicio}</td>
            <td class="p-3 text-emerald-400 font-mono tracking-wider text-sm">${formatoDinero.format(r.monto)}</td>
            <td class="p-3 text-emerald-300 font-mono text-xs">${r.propina > 0 ? '+' + formatoDinero.format(r.propina) : '—'}</td>
            <td class="p-3">${bPago}</td>
            <td class="p-3 text-right">${editBtn}</td>
        </tr>`;
    });

    // Totals
    const tot = document.getElementById('total-ingresos'); if(tot) tot.textContent = formatoDinero.format(tIngresos);
    const totEf = document.getElementById('total-efectivo'); if(totEf) totEf.textContent = formatoDinero.format(tEfectivo);
    const totTar = document.getElementById('total-tarjeta'); if(totTar) totTar.textContent = formatoDinero.format(tTarjeta);
    const totC = document.getElementById('total-cortes'); if(totC) totC.textContent = regsHoy.length;

    // Panel comisiones
    if(rolActual === 'admin') {
        const grid = document.getElementById('barberos-grid');
        if(grid) {
            grid.innerHTML = '';
            Object.keys(resBarb).sort().forEach(n => {
                const s = resBarb[n];
                grid.innerHTML += `<div class="border border-zinc-800 rounded-sm p-3 bg-zinc-950 flex flex-col">
                    <div class="flex justify-between items-center mb-2"><span class="font-bold text-zinc-200 text-sm">${n}</span><span class="text-xs bg-zinc-800 text-zinc-400 px-2 py-1 rounded-sm">${s.cortes} serv.</span></div>
                    <p class="text-xs text-zinc-500 flex justify-between">Comisión: <span class="text-emerald-400">${formatoDinero.format(s.comision)}</span></p>
                    <p class="text-xs text-zinc-500 flex justify-between">Propinas: <span class="text-emerald-300">${formatoDinero.format(s.propinas)}</span></p>
                    <div class="border-t border-zinc-800 mt-2 pt-2 flex justify-between font-bold"><span class="text-zinc-300 text-xs">Total:</span><span class="text-emerald-400">${formatoDinero.format(s.comision + s.propinas)}</span></div>
                </div>`;
            });
        }
    }

    // Update global vars for corte de caja
    window.totalIngresosDia = tIngresos;
    window.totalPropinasDia = tPropinas;
    window.totalPropinasEfvoDia = tPropinasEfvo;
    window.totalPropinasTarjDia = tPropinasTarj;
    window.ingresosEfvoActuales = tEfectivo;
    window.ingresosTarjetaActuales = tTarjeta;
    window.totalTicketsDia = regsHoy.length;
    const gastoTotal = gastosHoy.reduce((s, r) => s + r.monto, 0);
    window.gastosTotalesActuales = gastoTotal;
    window.cajaEfectivoActual = tEfectivo - tPropinas - gastoTotal;
}

function eliminarRegistro(id) {
    if(rolActual !== 'admin') return;
    mostrarConfirmacion('Eliminar Registro', '¿Borrar este registro? Afectará la caja y reportes.', () => {
        registros = registros.filter(r => r.id !== id);
        actualizarVistaHoy();
        if(document.getElementById('vista-reportes') && !document.getElementById('vista-reportes').classList.contains('hidden')) actualizarReportes();
    });
}

const btnLimpiar = document.getElementById('btn-limpiar');
if(btnLimpiar) btnLimpiar.addEventListener('click', () => {
    if(rolActual !== 'admin') return;
    const fecha = document.getElementById('filtro-fecha-pos')?.value;
    mostrarConfirmacion('Limpiar Bitácora', `¿Borrar TODOS los registros de ${fecha}? No se puede deshacer.`, () => {
        registros = registros.filter(r => r.fechaCorta !== fecha);
        actualizarVistaHoy();
    });
});

// ==========================================
// 5. TABS & NAVEGACIÓN
// ==========================================
window.cambiarTab = function(tab) {
    // SEGURIDAD ESTRICTA: Solo el Dueño / Admin tiene acceso a Administración
    if (tab === 'reportes' && rolActual !== 'admin') {
        tab = 'pos';
    }

    const tabs = ['pos', 'lealtad', 'inventario', 'reportes'];
    tabs.forEach(t => {
        const btn = document.getElementById('tab-' + t);
        const vista = document.getElementById('vista-' + t);
        if (btn) {
            if (t === 'reportes' && rolActual !== 'admin') {
                btn.classList.add('hidden');
                btn.style.display = 'none';
            } else {
                btn.classList.remove('hidden');
                btn.style.display = '';
                if (t === tab) {
                    btn.className = 'py-4 text-[11px] tracking-[0.15em] uppercase border-b-2 border-yellow-500 text-yellow-400 font-bold transition-colors whitespace-nowrap flex items-center gap-1.5';
                } else {
                    btn.className = 'py-4 text-[11px] tracking-[0.15em] uppercase border-b-2 border-transparent text-zinc-500 hover:text-zinc-300 font-medium transition-colors whitespace-nowrap flex items-center gap-1.5';
                }
            }
        }
        if (vista) {
            if (t === tab) vista.classList.remove('hidden');
            else vista.classList.add('hidden');
        }
    });

    if (tab === 'pos') {
        actualizarVistaHoy();
        actualizarSelectsForm();
    }
    if (tab === 'lealtad') actualizarUILealtad();
    if (tab === 'inventario') actualizarUIInventario();
    if (tab === 'reportes' && rolActual === 'admin') {
        if(!document.getElementById('reporte-desde')?.value) {
            document.getElementById('quick-date-select') && (document.getElementById('quick-date-select').value = 'este_mes');
            applyQuickDate();
        } else actualizarReportes();
    }
};

// ==========================================
// 5.1 LEALTAD Y CLIENTES
// ==========================================
window.recompensaLealtadAplicada = false;

window.cambiarMetaSellos = function(nuevaMeta) {
    const val = parseInt(nuevaMeta) || 5;
    metaSellos = Math.max(2, Math.min(20, val));
    guardarDatos();
    actualizarUILealtad();
    actualizarSelectClientesPOS();
};

window.buscarClienteLealtad = function() {
    const telInput = document.getElementById('cliente-telefono');
    const nomInput = document.getElementById('cliente-nombre');
    const badge = document.getElementById('badge-lealtad-cliente');
    const banner = document.getElementById('banner-recompensa-lealtad');
    if (!telInput) return;

    const val = telInput.value.trim();
    const selRapido = document.getElementById('cliente-select-existente');
    if (val.length < 3) {
        if(badge) badge.classList.add('hidden');
        if(banner) banner.classList.add('hidden');
        if(selRapido && !val) selRapido.value = '';
        return;
    }

    const match = clientesLealtad.find(c => c.telefono.includes(val) || (c.nombre && c.nombre.toLowerCase().includes(val.toLowerCase())));
    if (match) {
        if(nomInput && !nomInput.value) nomInput.value = match.nombre;
        if(selRapido) selRapido.value = match.telefono;
        if(badge) {
            badge.textContent = `⭐ ${match.sellos || 0}/${metaSellos} SELLOS`;
            badge.classList.remove('hidden');
        }
        if(banner) {
            if((match.sellos || 0) >= metaSellos) {
                banner.innerHTML = `
                    <div class="flex items-center gap-2">
                        <i class="fa-solid fa-crown text-yellow-400"></i>
                        <span>¡${metaSellos} sellos! Recompensa lista</span>
                    </div>
                    <button type="button" onclick="aplicarRecompensaLealtad()" class="px-2 py-0.5 bg-yellow-500 text-black font-bold text-[10px] rounded uppercase hover:bg-yellow-400 transition-colors">Aplicar</button>`;
                banner.classList.remove('hidden');
            } else {
                banner.classList.add('hidden');
            }
        }
    } else {
        if(badge) badge.classList.add('hidden');
        if(banner) banner.classList.add('hidden');
    }
};

window.aplicarRecompensaLealtad = function() {
    window.recompensaLealtadAplicada = true;
    const montoEl = document.getElementById('monto');
    if(montoEl) montoEl.value = '0';
    if(!serviciosActuales.includes(`🎁 Cortesía Lealtad (${metaSellos}/${metaSellos})`)) {
        serviciosActuales.unshift(`🎁 Cortesía Lealtad (${metaSellos}/${metaSellos})`);
        actualizarUISeleccion();
    }
    const banner = document.getElementById('banner-recompensa-lealtad');
    if(banner) banner.innerHTML = `<span class="text-emerald-400 font-bold"><i class="fa-solid fa-check"></i> ¡Cortesía aplicada con éxito al ticket ($0)!</span>`;
};

window.actualizarUILealtad = function() {
    const totCli = document.getElementById('lealtad-total-clientes');
    if(totCli) totCli.textContent = clientesLealtad.length;

    const recListas = clientesLealtad.filter(c => (c.sellos || 0) >= metaSellos).length;
    const recEl = document.getElementById('lealtad-recompensas-listas');
    if(recEl) recEl.textContent = recListas;

    const recLbl = document.getElementById('lealtad-label-recompensas');
    if(recLbl) recLbl.textContent = `Recompensas Listas (${metaSellos}/${metaSellos})`;

    const thProg = document.getElementById('th-progreso-sellos');
    if(thProg) thProg.textContent = `Progreso Sellos (${metaSellos} max)`;

    const selMeta = document.getElementById('select-meta-sellos');
    if(selMeta) selMeta.value = metaSellos;

    const totVisitas = clientesLealtad.reduce((acc, c) => acc + (c.visitas || 0), 0);
    const visEl = document.getElementById('lealtad-total-visitas');
    if(visEl) visEl.textContent = totVisitas;

    filtrarClientesUI();
};

window.filtrarClientesUI = function() {
    const tbody = document.getElementById('tabla-clientes-lealtad');
    if(!tbody) return;
    const q = (document.getElementById('filtro-cliente-input')?.value || '').toLowerCase().trim();

    const filtrados = clientesLealtad.filter(c => 
        c.nombre.toLowerCase().includes(q) || c.telefono.includes(q)
    );

    if(filtrados.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-6 text-center text-zinc-600 uppercase tracking-widest text-[10px]">No se encontraron clientes registrados.</td></tr>`;
        return;
    }

    tbody.innerHTML = '';
    filtrados.forEach(c => {
        const s = Math.min(metaSellos, Math.max(0, c.sellos || 0));
        const faltan = Math.max(0, metaSellos - s);
        const tijeras = '✂️'.repeat(s) + '⚪'.repeat(faltan);
        const badgeRecompensa = s >= metaSellos 
            ? `<span class="ml-2 px-1.5 py-0.5 bg-yellow-500/20 text-yellow-400 border border-yellow-500/40 rounded text-[9px] font-bold uppercase tracking-wider">¡Corte Gratis!</span>`
            : '';
        const desdeFmt = c.clienteDesde || c.fechaRegistro || c.ultimaVisita || '2026-11-01';

        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900/60 transition-colors">
                <td class="p-3.5 font-bold text-zinc-200">${c.nombre} ${badgeRecompensa}</td>
                <td class="p-3.5 font-mono text-zinc-400">${c.telefono}</td>
                <td class="p-3.5 font-mono text-zinc-400 text-xs">
                    <span class="inline-flex items-center gap-1.5 bg-zinc-900/80 px-2 py-0.5 rounded border border-zinc-800 text-zinc-300">
                        <i class="fa-regular fa-calendar text-yellow-500/80 text-[10px]"></i>
                        ${desdeFmt}
                    </span>
                </td>
                <td class="p-3.5 font-mono text-xs">
                    <span class="text-yellow-400 font-bold">${s}/${metaSellos}</span> 
                    <span class="ml-2 text-zinc-400 tracking-tight">${tijeras}</span>
                </td>
                <td class="p-3.5 font-mono text-zinc-300 font-bold">${c.visitas || 0}</td>
                <td class="p-3.5 font-mono text-zinc-500 text-xs">${c.ultimaVisita || '-'}</td>
                <td class="p-3.5 text-right space-x-1.5 whitespace-nowrap">
                    <button onclick="abrirModalTarjeta('${c.telefono}')" class="px-2.5 py-1 text-[10px] uppercase tracking-wider font-bold bg-yellow-950/40 text-yellow-400 border border-yellow-800/60 rounded hover:bg-yellow-900/50 transition-colors" title="Ver Pase Digital">
                        <i class="fa-solid fa-id-card mr-1"></i> Tarjeta
                    </button>
                    <button onclick="abrirModalTarjeta('${c.telefono}'); setTimeout(compartirTarjetaWhatsApp, 300)" class="px-2.5 py-1 text-[10px] uppercase tracking-wider font-bold bg-emerald-950/40 text-emerald-400 border border-emerald-800/60 rounded hover:bg-emerald-900/50 transition-colors" title="Compartir WhatsApp">
                        <i class="fa-brands fa-whatsapp mr-1"></i> WA
                    </button>
                    <button onclick="abrirModalEditarCliente('${c.telefono}')" class="px-2.5 py-1 text-[10px] uppercase tracking-wider font-bold bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-600 rounded transition-colors" title="Editar Información">
                        <i class="fa-solid fa-pen-to-square mr-1"></i> Editar
                    </button>
                </td>
            </tr>`;
    });
};

window.abrirModalNuevoCliente = function() {
    const m = document.getElementById('modal-cliente');
    if(!m) return;
    document.getElementById('modal-cliente-titulo').innerHTML = `<i class="fa-solid fa-user-plus text-yellow-500"></i> Añadir Nuevo Cliente`;
    document.getElementById('cli-modal-tel-original').value = '';
    document.getElementById('cli-modal-nombre').value = '';
    document.getElementById('cli-modal-telefono').value = '';
    
    const inpSellos = document.getElementById('cli-modal-sellos');
    if(inpSellos) {
        inpSellos.value = '1';
        inpSellos.max = metaSellos;
    }
    const lblSellos = document.getElementById('label-cli-modal-sellos');
    if(lblSellos) lblSellos.textContent = `Sellos (0 a ${metaSellos})`;
    
    document.getElementById('cli-modal-visitas').value = '1';

    const hoy = new Date().toISOString().split('T')[0];
    const inpDesde = document.getElementById('cli-modal-cliente-desde');
    if(inpDesde) inpDesde.value = hoy;

    const selSuc = document.getElementById('cli-modal-sucursal');
    if(selSuc) {
        selSuc.innerHTML = '';
        sucursalesActivas.forEach(s => selSuc.innerHTML += `<option value="${s}">${s}</option>`);
    }

    const btnDel = document.getElementById('btn-eliminar-cliente');
    if(btnDel) btnDel.classList.add('hidden');

    m.classList.remove('hidden');
};

window.abrirModalEditarCliente = function(tel) {
    const cli = clientesLealtad.find(c => c.telefono === tel);
    if(!cli) return;

    const m = document.getElementById('modal-cliente');
    if(!m) return;

    document.getElementById('modal-cliente-titulo').innerHTML = `<i class="fa-solid fa-user-pen text-yellow-500"></i> Editar Cliente: ${cli.nombre}`;
    document.getElementById('cli-modal-tel-original').value = cli.telefono;
    document.getElementById('cli-modal-nombre').value = cli.nombre;
    document.getElementById('cli-modal-telefono').value = cli.telefono;

    const inpSellos = document.getElementById('cli-modal-sellos');
    if(inpSellos) {
        inpSellos.value = Math.min(metaSellos, cli.sellos || 0);
        inpSellos.max = metaSellos;
    }
    const lblSellos = document.getElementById('label-cli-modal-sellos');
    if(lblSellos) lblSellos.textContent = `Sellos (0 a ${metaSellos})`;

    document.getElementById('cli-modal-visitas').value = cli.visitas || 0;

    const hoy = new Date().toISOString().split('T')[0];
    const inpDesde = document.getElementById('cli-modal-cliente-desde');
    if(inpDesde) inpDesde.value = cli.clienteDesde || cli.fechaRegistro || cli.ultimaVisita || hoy;

    const selSuc = document.getElementById('cli-modal-sucursal');
    if(selSuc) {
        selSuc.innerHTML = '';
        sucursalesActivas.forEach(s => {
            const isSel = (cli.sucursal === s) ? ' selected' : '';
            selSuc.innerHTML += `<option value="${s}"${isSel}>${s}</option>`;
        });
    }

    const btnDel = document.getElementById('btn-eliminar-cliente');
    if(btnDel) btnDel.classList.remove('hidden');

    m.classList.remove('hidden');
};

window.cerrarModalCliente = function() {
    const m = document.getElementById('modal-cliente');
    if(m) m.classList.add('hidden');
};

window.guardarClienteModal = function(e) {
    e.preventDefault();
    const telOrig = document.getElementById('cli-modal-tel-original')?.value?.trim();
    const nombre = document.getElementById('cli-modal-nombre')?.value?.trim();
    const telefono = document.getElementById('cli-modal-telefono')?.value?.trim();
    const sellos = Math.min(metaSellos, Math.max(0, parseInt(document.getElementById('cli-modal-sellos')?.value) || 0));
    const visitas = Math.max(0, parseInt(document.getElementById('cli-modal-visitas')?.value) || 0);
    const sucursal = document.getElementById('cli-modal-sucursal')?.value || sucursalActual;
    const clienteDesde = document.getElementById('cli-modal-cliente-desde')?.value?.trim() || new Date().toISOString().split('T')[0];

    if(!nombre || !telefono) return;

    if(telOrig) {
        // Editando cliente existente
        const cli = clientesLealtad.find(c => c.telefono === telOrig);
        if(cli) {
            cli.nombre = nombre;
            cli.telefono = telefono;
            cli.sellos = sellos;
            cli.visitas = visitas;
            cli.sucursal = sucursal;
            cli.clienteDesde = clienteDesde;
        }
    } else {
        // Nuevo cliente
        const existe = clientesLealtad.find(c => c.telefono === telefono);
        if(existe) {
            existe.nombre = nombre;
            existe.sellos = sellos;
            existe.visitas = visitas;
            existe.sucursal = sucursal;
            existe.clienteDesde = clienteDesde;
        } else {
            clientesLealtad.unshift({
                telefono,
                nombre,
                sellos,
                visitas,
                sucursal,
                clienteDesde,
                ultimaVisita: new Date().toISOString().split('T')[0],
                historial: []
            });
        }
    }

    guardarDatos();
    cerrarModalCliente();
    actualizarUILealtad();
    actualizarSelectClientesPOS();
};

window.eliminarClienteModal = function() {
    const telOrig = document.getElementById('cli-modal-tel-original')?.value?.trim();
    if(!telOrig) return;
    mostrarConfirmacion('Eliminar Cliente', '¿Seguro que deseas eliminar este cliente del club de lealtad?', () => {
        clientesLealtad = clientesLealtad.filter(c => c.telefono !== telOrig);
        guardarDatos();
        cerrarModalCliente();
        actualizarUILealtad();
        actualizarSelectClientesPOS();
    });
};

let clienteTarjetaActivo = null;
window.abrirModalTarjeta = function(tel) {
    const cli = clientesLealtad.find(c => c.telefono === tel);
    if(!cli) return;
    clienteTarjetaActivo = cli;

    const m = document.getElementById('modal-tarjeta-lealtad');
    if(!m) return;

    document.getElementById('tarjeta-sucursal').textContent = cli.sucursal || sucursalActual;
    document.getElementById('tarjeta-cliente-nombre').textContent = cli.nombre || 'Cliente VIP';
    document.getElementById('tarjeta-cliente-telefono').textContent = cli.telefono.replace(/(\d{2})(\d{4})(\d{4})/, '$1 $2 $3');

    const desdeTxt = document.getElementById('tarjeta-cliente-desde');
    if(desdeTxt) desdeTxt.textContent = cli.clienteDesde || cli.fechaRegistro || cli.ultimaVisita || '2026-11-01';

    const sellos = Math.min(metaSellos, Math.max(0, cli.sellos || 0));
    document.getElementById('tarjeta-sellos-contador').textContent = `${sellos} / ${metaSellos}`;

    const grid = document.getElementById('tarjeta-sellos-grid');
    if(grid) {
        grid.innerHTML = '';
        for(let i = 1; i <= metaSellos; i++) {
            if(i <= sellos) {
                grid.innerHTML += `
                    <div class="flex-1 aspect-square rounded-xl bg-gradient-to-tr from-yellow-600 to-yellow-400 text-black flex flex-col items-center justify-center font-bold shadow-lg shadow-yellow-500/20 transform scale-105 transition-transform">
                        <i class="fa-solid fa-scissors text-sm"></i>
                        <span class="text-[8px] mt-0.5 font-mono">#${i}</span>
                    </div>`;
            } else {
                grid.innerHTML += `
                    <div class="flex-1 aspect-square rounded-xl border border-dashed border-zinc-700 bg-zinc-900/50 text-zinc-600 flex flex-col items-center justify-center font-mono">
                        <i class="fa-solid fa-circle text-[8px] opacity-30"></i>
                        <span class="text-[8px] mt-0.5 opacity-40">#${i}</span>
                    </div>`;
            }
        }
    }

    const recTxt = document.getElementById('tarjeta-recompensa-texto');
    if(recTxt) {
        recTxt.textContent = sellos >= metaSellos 
            ? '🎉 ¡META ALCANZADA! Muestra esta tarjeta para tu corte gratis' 
            : `⭐ Faltan ${metaSellos - sellos} visitas para tu corte de cortesía`;
    }

    // QR Code
    const qrContainer = document.getElementById('qrcode-tarjeta');
    if(qrContainer) {
        qrContainer.innerHTML = '';
        if(typeof QRCode !== 'undefined') {
            new QRCode(qrContainer, {
                text: `MB-VIP:${cli.telefono}`,
                width: 120,
                height: 120,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.M
            });
        }
    }

    m.classList.remove('hidden');
};

window.cerrarModalTarjeta = function() {
    const m = document.getElementById('modal-tarjeta-lealtad');
    if(m) m.classList.add('hidden');
    clienteTarjetaActivo = null;
};

window.compartirTarjetaWhatsApp = function() {
    if(!clienteTarjetaActivo) return;
    const c = clienteTarjetaActivo;
    const s = Math.min(metaSellos, c.sellos || 0);
    const faltan = Math.max(0, metaSellos - s);
    const tijeras = '✂️'.repeat(s) + '⚪'.repeat(faltan);
    let msg = `💈 *TARJETA DIGITAL DE LEALTAD - MB BARBEROS* 💈\n`;
    msg += `👤 *Titular:* ${c.nombre}\n`;
    msg += `📱 *Tel:* ${c.telefono}\n`;
    msg += `📅 *Cliente desde:* ${c.clienteDesde || c.ultimaVisita || '-'}\n`;
    msg += `⭐ *Sellos:* ${s} de ${metaSellos} ${tijeras}\n`;
    msg += s >= metaSellos ? `🎉 *¡Tienes corte de cortesía disponible!*\n` : `_Faltan ${faltan} visitas para tu corte gratis._\n`;
    msg += `📍 *Sucursal:* ${c.sucursal || sucursalActual}\n`;
    const tel = c.telefono.replace(/\D/g, '');
    window.open(`https://wa.me/52${tel}?text=${encodeURIComponent(msg)}`, '_blank');
};

// ==========================================
// 5.2 TICKET DIGITAL WHATSAPP
// ==========================================
let ticketDigitalActual = null;
window.abrirModalTicketDigital = function(datos) {
    ticketDigitalActual = datos;
    const m = document.getElementById('modal-ticket-digital');
    if(!m) return;
    
    document.getElementById('ticket-dig-fecha').textContent = datos.fecha + ' (' + datos.sucursal + ')';
    document.getElementById('ticket-dig-barbero').textContent = datos.barbero;
    document.getElementById('ticket-dig-servicio').textContent = datos.servicio;
    document.getElementById('ticket-dig-total').textContent = formatoDinero.format(datos.total);
    document.getElementById('ticket-dig-pago').textContent = datos.pago;

    const boxLealtad = document.getElementById('ticket-dig-lealtad-box');
    const btnVerTarjeta = document.getElementById('btn-ticket-ver-tarjeta');
    if (datos.cliente) {
        if(boxLealtad) {
            boxLealtad.classList.remove('hidden');
            const s = Math.min(metaSellos, datos.cliente.sellos || 1);
            const faltan = Math.max(0, metaSellos - s);
            const tijeras = '✂️'.repeat(s) + '⚪'.repeat(faltan);
            document.getElementById('ticket-dig-lealtad-txt').textContent = `⭐ Sellos: ${s} de ${metaSellos}  ${tijeras}`;
            document.getElementById('ticket-dig-lealtad-sub').textContent = s >= metaSellos ? '🎉 ¡Recompensa lista para el próximo corte!' : `Faltan ${faltan} visitas para recompensa de lealtad`;
        }
        if(btnVerTarjeta) btnVerTarjeta.classList.remove('hidden');
    } else {
        if(boxLealtad) boxLealtad.classList.add('hidden');
        if(btnVerTarjeta) btnVerTarjeta.classList.add('hidden');
    }

    m.classList.remove('hidden');
};

window.cerrarModalTicketDigital = function() {
    const m = document.getElementById('modal-ticket-digital');
    if(m) m.classList.add('hidden');
    ticketDigitalActual = null;
};

window.ejecutarEnvioWhatsAppTicket = function() {
    if(!ticketDigitalActual) return;
    const t = ticketDigitalActual;
    let msg = `💈 *MB BARBEROS - COMPROBANTE DE SERVICIO* 💈\n`;
    msg += `📍 *Sucursal:* ${t.sucursal}\n`;
    msg += `📅 *Fecha:* ${t.fecha}\n`;
    msg += `✂️ *Barbero:* ${t.barbero}\n\n`;
    msg += `🧾 *Servicio(s):* ${t.servicio}\n`;
    msg += `💰 *Total Pagado:* ${formatoDinero.format(t.total)} (${t.pago})\n\n`;

    if(t.cliente) {
        const s = Math.min(metaSellos, t.cliente.sellos || 1);
        const faltan = Math.max(0, metaSellos - s);
        const tijeras = '✂️'.repeat(s) + '⚪'.repeat(faltan);
        msg += `⭐ *PROGRAMA DE LEALTAD VIP:*\n`;
        msg += `Has acumulado *${s} de ${metaSellos} sellos* ${tijeras}\n`;
        if(s >= metaSellos) {
            msg += `🎉 *¡Felicidades! Tienes un servicio de cortesía disponible para tu próxima visita.*\n`;
        } else {
            msg += `_¡Solo te faltan ${faltan} visitas para tu corte de cortesía!_\n`;
        }
        msg += `\n`;
    }

    msg += `_¡Gracias por tu preferencia en Studio MB!_\n`;

    const tel = t.cliente?.telefono ? t.cliente.telefono.replace(/\D/g, '') : '';
    const url = tel.length === 10 ? `https://wa.me/52${tel}?text=${encodeURIComponent(msg)}` : `https://wa.me/?text=${encodeURIComponent(msg)}`;
    window.open(url, '_blank');
};

window.verTarjetaDesdeTicket = function() {
    if(ticketDigitalActual && ticketDigitalActual.cliente) {
        window.abrirModalTarjeta(ticketDigitalActual.cliente.telefono);
    }
};

// ==========================================
// 5.3 INVENTARIO DE PRODUCTOS
// ==========================================
window.actualizarUIInventario = function() {
    const totProd = document.getElementById('inv-total-productos');
    if(totProd) totProd.textContent = inventarioProductos.length;

    const suc = sucursalActual === 'Todas' ? 'La Morena' : sucursalActual;
    const labelSuc = document.getElementById('inv-label-sucursal');
    if(labelSuc) labelSuc.textContent = `Stock en ${suc}`;

    let piezasTienda = 0;
    let bajas = 0;
    inventarioProductos.forEach(p => {
        const s = (p.stock && p.stock[suc] !== undefined) ? p.stock[suc] : 0;
        piezasTienda += s;
        if(s <= (p.stockMinimo || 3)) bajas++;
    });

    const piezasEl = document.getElementById('inv-piezas-tienda');
    if(piezasEl) piezasEl.textContent = piezasTienda;

    const bajoEl = document.getElementById('inv-alertas-bajo');
    if(bajoEl) bajoEl.textContent = bajas;

    const tbody = document.getElementById('tabla-inventario-body');
    if(!tbody) return;

    tbody.innerHTML = '';
    inventarioProductos.forEach(p => {
        const stockActual = (p.stock && p.stock[suc] !== undefined) ? p.stock[suc] : 0;
        const min = p.stockMinimo || 3;
        
        let estadoBadge = '';
        if(stockActual === 0) {
            estadoBadge = `<span class="px-2 py-0.5 bg-red-950 text-red-400 border border-red-800 rounded text-[9px] uppercase tracking-widest font-bold">Agotado</span>`;
        } else if(stockActual <= min) {
            estadoBadge = `<span class="px-2 py-0.5 bg-yellow-950 text-yellow-400 border border-yellow-800 rounded text-[9px] uppercase tracking-widest font-bold">Stock Bajo</span>`;
        } else {
            estadoBadge = `<span class="px-2 py-0.5 bg-emerald-950 text-emerald-400 border border-emerald-800 rounded text-[9px] uppercase tracking-widest font-bold">En Stock</span>`;
        }

        let breakdownStocks = '';
        sucursalesActivas.forEach(sName => {
            const qty = p.stock ? (p.stock[sName] || 0) : 0;
            const isCur = sName === suc;
            breakdownStocks += `<span class="text-[10px] font-mono px-1.5 py-0.5 rounded ${isCur ? 'bg-zinc-800 text-white font-bold border border-zinc-600' : 'text-zinc-500'}">${sName}: ${qty}</span> `;
        });

        tbody.innerHTML += `
            <tr class="hover:bg-zinc-900/60 transition-colors">
                <td class="p-3.5 font-bold text-zinc-200">
                    ${p.nombre}
                </td>
                <td class="p-3.5 font-mono text-emerald-400 font-bold">${formatoDinero.format(p.precio)}</td>
                <td class="p-3.5">
                    <div class="flex flex-wrap gap-1">${breakdownStocks}</div>
                </td>
                <td class="p-3.5 font-mono text-zinc-500">${min} pzs</td>
                <td class="p-3.5">${estadoBadge}</td>
                <td class="p-3.5 text-right space-x-1">
                    <button onclick="ajustarStock('${p.nombre}', '${suc}', -1)" class="w-7 h-7 bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 font-bold rounded text-xs transition-colors">-1</button>
                    <button onclick="ajustarStock('${p.nombre}', '${suc}', 1)" class="w-7 h-7 bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-emerald-400 font-bold rounded text-xs transition-colors">+1</button>
                    <button onclick="ajustarStock('${p.nombre}', '${suc}', 5)" class="px-2 h-7 bg-blue-950 hover:bg-blue-900 border border-blue-800 text-blue-300 font-bold rounded text-xs transition-colors">+5</button>
                </td>
            </tr>`;
    });
};

window.ajustarStock = function(prodNombre, suc, delta) {
    const prod = inventarioProductos.find(p => p.nombre === prodNombre);
    if(!prod) return;
    if(!prod.stock) prod.stock = {};
    prod.stock[suc] = Math.max(0, (prod.stock[suc] || 0) + delta);
    guardarDatos();
    actualizarUIInventario();
    actualizarSelectsForm();
};

window.abrirModalNuevoProducto = function() {
    const m = document.getElementById('modal-nuevo-producto');
    if(!m) return;
    const grid = document.getElementById('nuevo-prod-stocks-grid');
    if(grid) {
        grid.innerHTML = '';
        sucursalesActivas.forEach(s => {
            grid.innerHTML += `
                <div>
                    <label class="block text-[10px] text-zinc-500 font-bold uppercase mb-1">${s}</label>
                    <input type="number" id="nuevo-stock-${s}" value="10" min="0" class="w-full input-dark rounded-sm p-2 text-xs">
                </div>`;
        });
    }
    m.classList.remove('hidden');
};

window.cerrarModalNuevoProducto = function() {
    const m = document.getElementById('modal-nuevo-producto');
    if(m) m.classList.add('hidden');
    const f = document.getElementById('form-nuevo-producto');
    if(f) f.reset();
};

window.guardarNuevoProducto = function(e) {
    e.preventDefault();
    const nombre = document.getElementById('nuevo-prod-nombre')?.value?.trim();
    const precio = parseFloat(document.getElementById('nuevo-prod-precio')?.value) || 0;
    const minimo = parseInt(document.getElementById('nuevo-prod-minimo')?.value) || 3;
    if(!nombre) return;

    const stocks = {};
    sucursalesActivas.forEach(s => {
        stocks[s] = parseInt(document.getElementById(`nuevo-stock-${s}`)?.value) || 0;
    });

    inventarioProductos.push({
        id: Date.now(),
        nombre,
        precio,
        stockMinimo: minimo,
        stock: stocks
    });

    if(!productosActivos.includes(nombre)) productosActivos.push(nombre);
    preciosBase[nombre] = precio;

    guardarDatos();
    cerrarModalNuevoProducto();
    actualizarUIInventario();
    actualizarSelectsForm();
};

// ==========================================
// 6. REPORTES
// ==========================================
function applyQuickDate() {
    const sel = document.getElementById('quick-date-select');
    if(!sel || sel.value === 'custom') return;
    const val = sel.value;
    const now = new Date();
    let desde = new Date(), hasta = new Date();
    if(val === 'este_mes') { desde = new Date(now.getFullYear(), now.getMonth(), 1); hasta = new Date(now.getFullYear(), now.getMonth() + 1, 0); }
    else if(val === 'mes_pasado') { desde = new Date(now.getFullYear(), now.getMonth()-1, 1); hasta = new Date(now.getFullYear(), now.getMonth(), 0); }
    else if(val === 'esta_semana') { const d = now.getDay()||7; desde = new Date(now); desde.setDate(now.getDate()-d+1); hasta = new Date(desde); hasta.setDate(desde.getDate()+6); }
    else if(val === 'semana_pasada') { const d = now.getDay()||7; hasta = new Date(now); hasta.setDate(now.getDate()-d); desde = new Date(hasta); desde.setDate(hasta.getDate()-6); }
    const tOff = desde.getTimezoneOffset()*60000;
    const dEl = document.getElementById('reporte-desde');
    const hEl = document.getElementById('reporte-hasta');
    if(dEl) dEl.value = new Date(desde-tOff).toISOString().split('T')[0];
    if(hEl) hEl.value = new Date(hasta-tOff).toISOString().split('T')[0];
    actualizarReportes();
}

const desdEl = document.getElementById('reporte-desde');
const hastaEl = document.getElementById('reporte-hasta');
const btnFilt = document.getElementById('btn-filtrar-reportes');
const qSel = document.getElementById('quick-date-select');
if(desdEl) desdEl.addEventListener('change', () => { if(qSel) qSel.value='custom'; });
if(hastaEl) hastaEl.addEventListener('change', () => { if(qSel) qSel.value='custom'; });
if(btnFilt) btnFilt.addEventListener('click', actualizarReportes);

function actualizarReportes() {
    if(rolActual !== 'admin') return;
    const dEl = document.getElementById('reporte-desde');
    const hEl = document.getElementById('reporte-hasta');
    if(!dEl || !hEl || !dEl.value || !hEl.value) return;
    const dateDesde = new Date(dEl.value + 'T00:00:00');
    const dateHasta = new Date(hEl.value + 'T23:59:59');
    let regsPeriodo = registros.filter(r => r.tipo !== 'Gasto' && r.fechaObj >= dateDesde && r.fechaObj <= dateHasta);
    if(sucursalActual !== 'Todas') regsPeriodo = regsPeriodo.filter(r => r.sucursal === sucursalActual);
    const pagosPeriodo = pagosNomina.filter(p => p.fechaObj >= dateDesde && p.fechaObj <= dateHasta);

    const tIng = regsPeriodo.reduce((s,r) => s+r.monto, 0);
    const tPag = pagosPeriodo.reduce((s,p) => s+p.monto, 0);
    const repIng = document.getElementById('rep-ingresos-periodo'); if(repIng) repIng.textContent = formatoDinero.format(tIng);
    const repC = document.getElementById('rep-cortes-periodo'); if(repC) repC.textContent = regsPeriodo.length;
    const repProp = document.getElementById('rep-propina-promedio'); if(repProp) repProp.textContent = formatoDinero.format(regsPeriodo.length > 0 ? regsPeriodo.reduce((s,r)=>s+(r.propina||0),0)/regsPeriodo.length : 0);
    const repPagos = document.getElementById('rep-pagos-periodo'); if(repPagos) repPagos.textContent = formatoDinero.format(tPag);

    // Tendencia
    const mapFechas = {};
    regsPeriodo.forEach(r => { if(!mapFechas[r.fechaCorta]) mapFechas[r.fechaCorta]=0; mapFechas[r.fechaCorta]+=r.monto; });
    const labelsTend = Object.keys(mapFechas).sort();
    const datosTend = labelsTend.map(f => mapFechas[f]);

    // Nómina
    const barberosLocal = barberosActivos
        .filter(b => sucursalActual === 'Todas' || b.sucursal === sucursalActual)
        .map(b => typeof b === 'string' ? b : b.nombre);
    const mapBarberos = {};
    const mapNomina = {};
    barberosLocal.forEach(b => mapNomina[b] = { ventasBrutas: 0, sueldo: 0, propinasTotal: 0, pagado: 0 });

    regsPeriodo.forEach(r => {
        let montoProductos = 0;
        (r.servicio || '').split(' + ').forEach(item => {
            if(productosActivos.includes(item)) montoProductos += (preciosBase[item] || 0);
        });
        const montoComisionable = Math.max(0, r.monto - montoProductos);
        const prop = r.propina || 0;
        const comision = montoComisionable * 0.5;
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0;
        mapBarberos[r.barbero] += comision + prop;
        if(mapNomina[r.barbero]) {
            mapNomina[r.barbero].ventasBrutas += r.monto;
            mapNomina[r.barbero].sueldo += comision;
            mapNomina[r.barbero].propinasTotal += prop;
        }
    });
    pagosPeriodo.forEach(p => { if(mapNomina[p.barbero]) mapNomina[p.barbero].pagado += p.monto; });

    const tbodyNom = document.getElementById('tabla-nomina-barberos');
    if(tbodyNom) {
        tbodyNom.innerHTML = '';
        let totV=0, totS=0, totPr=0, totPag=0, totSaldo=0;
        Object.keys(mapNomina).sort().forEach(b => {
            const st = mapNomina[b];
            const saldo = (st.sueldo + st.propinasTotal) - st.pagado;
            if(st.ventasBrutas === 0 && st.sueldo === 0 && st.propinasTotal === 0 && st.pagado === 0) return;
            totV += st.ventasBrutas; totS += st.sueldo; totPr += st.propinasTotal; totPag += st.pagado; totSaldo += saldo;
            tbodyNom.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors">
                <td class="p-4 font-medium text-left text-zinc-200">${b}</td>
                <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono">${formatoDinero.format(st.ventasBrutas)}</td>
                <td class="p-4 text-center border-l border-zinc-900 bg-emerald-950/10">
                    <div class="flex flex-col items-center">
                        <span class="text-emerald-400 font-mono font-bold">${formatoDinero.format(st.sueldo)}</span>
                        <span class="text-[10px] text-zinc-500 uppercase tracking-widest">+ ${formatoDinero.format(st.propinasTotal)} prop.</span>
                    </div>
                </td>
                <td class="p-4 text-center border-l border-zinc-900 text-blue-400 font-mono">${formatoDinero.format(st.pagado)}</td>
                <td class="p-4 text-right border-l border-zinc-900 font-mono ${saldo > 0 ? 'text-red-400 font-bold' : 'text-zinc-500'}">${formatoDinero.format(saldo)}</td>
                <td class="p-4 text-center"><button onclick="abrirModalLiquidacion('${b}', ${saldo})" class="bg-emerald-950 text-emerald-500 border border-emerald-900 hover:bg-emerald-900 px-3 py-1 rounded-sm text-[10px] tracking-widest uppercase">Liquidar</button></td>
            </tr>`;
        });
        if(totV > 0) tbodyNom.innerHTML += `<tr class="bg-zinc-950 border-t border-zinc-800 font-bold">
            <td class="p-4 text-zinc-300 text-[10px] tracking-widest uppercase">Totales</td>
            <td class="p-4 text-center border-l border-zinc-900 text-zinc-500 font-mono">${formatoDinero.format(totV)}</td>
            <td class="p-4 text-center border-l border-zinc-900 text-emerald-500 font-mono"><div class="flex flex-col items-center"><span>${formatoDinero.format(totS)}</span><span class="text-[10px] text-zinc-500">+${formatoDinero.format(totPr)}</span></div></td>
            <td class="p-4 text-center border-l border-zinc-900 text-blue-500 font-mono">${formatoDinero.format(totPag)}</td>
            <td class="p-4 text-right border-l border-zinc-900 text-red-500 font-mono">${formatoDinero.format(totSaldo)}</td>
            <td class="p-4"></td>
        </tr>`;
    }

    const tbodyPagos = document.getElementById('tabla-historial-pagos');
    if(tbodyPagos) {
        tbodyPagos.innerHTML = '';
        if(pagosPeriodo.length === 0) { tbodyPagos.innerHTML = `<tr><td colspan="4" class="p-6 text-center text-zinc-600">No hay pagos en este periodo.</td></tr>`; }
        let totalPagadoHistorial = 0;
        [...pagosPeriodo].sort((a,b) => b.fechaObj-a.fechaObj).forEach(p => {
            totalPagadoHistorial += p.monto;
            tbodyPagos.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors"><td class="p-3 text-zinc-500">${p.fechaStr}</td><td class="p-3 font-bold text-zinc-200">${p.barbero}</td><td class="p-3 text-emerald-400 font-mono font-bold">${formatoDinero.format(p.monto)}</td><td class="p-3 text-zinc-400">${p.metodo}</td></tr>`;
        });
        if(pagosPeriodo.length > 0) {
            tbodyPagos.innerHTML += `<tr class="bg-zinc-950 border-t border-zinc-800 font-bold"><td colspan="2" class="p-3 text-right text-zinc-300 text-[10px] tracking-widest uppercase">Total Pagado:</td><td class="p-3 text-emerald-400 font-mono font-bold text-left">${formatoDinero.format(totalPagadoHistorial)}</td><td></td></tr>`;
        }
    }

    // Tabla Ediciones
    const tbodyEdiciones = document.getElementById('tabla-historial-ediciones');
    if(tbodyEdiciones) {
        tbodyEdiciones.innerHTML = '';
        const edicsPeriodo = historialEdiciones.filter(e => {
            const fd = e.fecha.split(',')[0].split('/'); // DD/MM/YYYY
            const d = new Date(fd[2], fd[1]-1, fd[0]);
            return d >= dateDesde && d <= dateHasta;
        });
        if(edicsPeriodo.length === 0) {
            tbodyEdiciones.innerHTML = `<tr><td colspan="4" class="p-6 text-center text-zinc-600">No hay modificaciones en este periodo.</td></tr>`;
        } else {
            edicsPeriodo.forEach(e => {
                tbodyEdiciones.innerHTML += `<tr class="hover:bg-zinc-900 transition-colors">
                    <td class="p-3 text-zinc-500 whitespace-nowrap">${e.fecha}<br><span class="text-orange-400 text-[9px] uppercase">${e.usuario}</span></td>
                    <td class="p-3 text-zinc-300 font-bold">${e.ticketInfo}</td>
                    <td class="p-3 text-red-400 text-xs">${e.antes}</td>
                    <td class="p-3 text-emerald-400 text-xs">${e.despues}</td>
                </tr>`;
            });
        }
    }

    // Charts
    const isDark = true;
    const cT = '#9ca3af'; const cG = '#27272a';
    const chartTend = document.getElementById('chartTendencia');
    const chartBarb = document.getElementById('chartBarberos');
    if(chartTend && typeof Chart !== 'undefined') {
        if(chartTendenciaInst) chartTendenciaInst.destroy();
        chartTendenciaInst = new Chart(chartTend.getContext('2d'), { type: 'line', data: { labels: labelsTend, datasets: [{ data: datosTend, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,0.1)', borderWidth: 3, tension: 0.4, fill: true }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: cG }, ticks: { color: cT } }, x: { grid: { display: false }, ticks: { color: cT } } } } });
    }
    if(chartBarb && typeof Chart !== 'undefined') {
        if(chartBarberosInst) chartBarberosInst.destroy();
        chartBarberosInst = new Chart(chartBarb.getContext('2d'), { type: 'bar', data: { labels: Object.keys(mapBarberos), datasets: [{ data: Object.values(mapBarberos), backgroundColor: '#eab308', borderRadius: 4 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, grid: { color: cG }, ticks: { color: cT } }, x: { grid: { display: false }, ticks: { color: cT } } } } });
    }
}

// ==========================================
// 7. PAGOS A BARBEROS / LIQUIDACIÓN
// ==========================================
const modalPago = document.getElementById('modal-pago');
window.toggleMixtoNomina = function(val) {
    const p = document.getElementById('panel-mixto-nomina');
    if(p) {
        if(val === 'Mixto') {
            p.classList.remove('hidden');
            calcularTransferenciaNomina();
        } else {
            p.classList.add('hidden');
        }
    }
};

window.calcularTransferenciaNomina = function() {
    const m = parseFloat(document.getElementById('pago-monto')?.value) || 0;
    const ef = parseFloat(document.getElementById('pago-efectivo-mixto')?.value) || 0;
    const tf = document.getElementById('pago-transferencia-mixto');
    if(tf) tf.value = Math.max(0, m - ef);
};

window.abrirModalLiquidacion = function(barbero, saldo) { abrirModalPago(barbero, Math.max(0, saldo)); };
function abrirModalPago(barbero, saldoPendiente) {
    if(!modalPago) return;
    const bn = document.getElementById('pago-barbero-nombre'); if(bn) bn.value = barbero;
    const bm = document.getElementById('pago-monto'); if(bm) { bm.value = saldoPendiente; bm.addEventListener('input', calcularTransferenciaNomina); }
    const bmet = document.getElementById('pago-metodo'); if(bmet) bmet.value = 'Efectivo';
    const pmn = document.getElementById('panel-mixto-nomina'); if(pmn) pmn.classList.add('hidden');
    modalPago.classList.remove('hidden');
}
window.cerrarModalPago = function() { if(modalPago) modalPago.classList.add('hidden'); };

const formPago = document.getElementById('form-pago-barbero');
if(formPago) formPago.addEventListener('submit', e => {
    e.preventDefault();
    const now = new Date();
    const barbero = document.getElementById('pago-barbero-nombre')?.value;
    const monto = parseFloat(document.getElementById('pago-monto')?.value) || 0;
    const metodo = document.getElementById('pago-metodo')?.value || 'Efectivo';
    const hastaStr = document.getElementById('reporte-hasta')?.value || now.toISOString().split('T')[0];
    const fechaPago = new Date(hastaStr + 'T12:00:00');
    
    if (metodo === 'Mixto') {
        const mEf = parseFloat(document.getElementById('pago-efectivo-mixto')?.value) || 0;
        const mTr = parseFloat(document.getElementById('pago-transferencia-mixto')?.value) || 0;
        if(mEf > 0) pagosNomina.unshift({ id: Date.now(), fechaObj: fechaPago, fechaStr: fechaPago.toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric'}), barbero, monto: mEf, metodo: 'Efectivo' });
        if(mTr > 0) pagosNomina.unshift({ id: Date.now()+1, fechaObj: fechaPago, fechaStr: fechaPago.toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric'}), barbero, monto: mTr, metodo: 'Transferencia' });
    } else {
        pagosNomina.unshift({ id: Date.now(), fechaObj: fechaPago, fechaStr: fechaPago.toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric'}), barbero, monto, metodo });
    }
    
    guardarDatos();
    window.cerrarModalPago();
    actualizarReportes();
});

// ==========================================
// 8. EDITAR / BORRAR TICKETS
// ==========================================
const modalEditar = document.getElementById('modal-editar');
window.abrirModalEditar = function(id) {
    const reg = registros.find(r => r.id === id);
    if(!reg || !modalEditar) return;
    ticketEnEdicion = reg.id;
    const btnDel = document.getElementById('btn-delete-ticket');
    if(btnDel) { if(rolActual === 'admin') btnDel.classList.remove('hidden'); else btnDel.classList.add('hidden'); }
    const ftx = document.getElementById('edit-fields-ticket');
    const fgas = document.getElementById('edit-fields-gasto');
    if(reg.tipo === 'Gasto') {
        if(ftx) ftx.classList.add('hidden'); if(fgas) fgas.classList.remove('hidden');
        const egc = document.getElementById('edit-gasto-concepto'); if(egc) egc.value = reg.servicio;
        const egm = document.getElementById('edit-gasto-monto'); if(egm) egm.value = reg.monto;
    } else {
        if(ftx) ftx.classList.remove('hidden'); if(fgas) fgas.classList.add('hidden');
        const eb = document.getElementById('edit-barbero'); if(eb) eb.value = reg.barbero;
        editServiciosActuales = reg.servicio ? reg.servicio.split(' + ').filter(s => s !== 'Ninguno') : [];
        actualizarUISeleccionEdit();
        const ebed = document.getElementById('edit-bebida'); if(ebed) ebed.value = reg.bebida === '-' ? '' : (reg.bebida || '');
        const em = document.getElementById('edit-monto'); if(em) em.value = reg.monto;
        const ep = document.getElementById('edit-propina'); if(ep) ep.value = reg.propina || 0;
        const epago = document.getElementById('edit-pago'); if(epago) { epago.value = reg.pagoTxt; epago.addEventListener('change', window.toggleMixtoEdit); window.toggleMixtoEdit(); }
    }
    modalEditar.classList.remove('hidden');
};
window.cerrarModalEditar = function() { ticketEnEdicion = null; if(modalEditar) modalEditar.classList.add('hidden'); };

window.toggleMixtoEdit = function() {
    const pagoSel = document.getElementById('edit-pago');
    const p = document.getElementById('edit-panel-mixto');
    if(p && pagoSel) {
        if(pagoSel.value === 'Mixto') {
            p.classList.remove('hidden');
            window.calcularRestanteMixtoEdit();
        } else {
            p.classList.add('hidden');
        }
    }
};

window.calcularRestanteMixtoEdit = function() {
    const p = document.getElementById('edit-panel-mixto');
    if(!p || p.classList.contains('hidden')) return;
    const m = parseFloat(document.getElementById('edit-monto')?.value) || 0;
    const pr = parseFloat(document.getElementById('edit-propina')?.value) || 0;
    const total = m + pr;
    const lbl = document.getElementById('edit-total-mixto-label');
    if(lbl) lbl.textContent = formatoDinero.format(total);
    
    const ef = parseFloat(document.getElementById('edit-monto-efectivo-mixto')?.value) || 0;
    const rest = Math.max(0, total - ef);
    const rlbl = document.getElementById('edit-restante-tarjeta-label');
    if(rlbl) rlbl.textContent = formatoDinero.format(rest);
};
window.borrarTicketEnEdicion = function() {
    if(rolActual !== 'admin') return;
    mostrarConfirmacion('Borrar Registro', '¿Estás seguro? Esta acción no se puede deshacer.', () => {
        registros = registros.filter(r => r.id !== ticketEnEdicion);
        window.cerrarModalEditar(); actualizarVistaHoy();
        if(vistaRep && !vistaRep.classList.contains('hidden')) actualizarReportes();
    });
};

function actualizarUISeleccionEdit() {
    const div = document.getElementById('edit-servicios-seleccionados');
    if(!div) return;
    if(editServiciosActuales.length === 0) { div.classList.add('hidden'); return; }
    div.classList.remove('hidden');
    div.innerHTML = editServiciosActuales.map(s => `<span class="inline-flex items-center gap-1 px-2 py-1 bg-zinc-800 border border-zinc-700 text-zinc-200 text-xs rounded-sm">${s} <button type="button" onclick="quitarServicioEdit('${s}')" class="text-zinc-500 hover:text-red-400">×</button></span>`).join('');
}
window.quitarServicioEdit = function(s) { editServiciosActuales = editServiciosActuales.filter(x => x !== s); actualizarUISeleccionEdit(); };
window.agregarServicioEdit = function() {
    const sel = document.getElementById('edit-servicio');
    if(sel && sel.value && !editServiciosActuales.includes(sel.value)) { editServiciosActuales.push(sel.value); actualizarUISeleccionEdit(); }
};

const formEdit = document.getElementById('form-editar-ticket');
if(formEdit) formEdit.addEventListener('submit', e => {
    e.preventDefault();
    if(!ticketEnEdicion) return;
    const reg = registros.find(r => r.id === ticketEnEdicion);
    if(reg) {
        let oldStr = reg.tipo === 'Gasto' 
            ? `Gasto: ${reg.servicio} | $${reg.monto}` 
            : `${reg.barbero} | $${reg.monto} | Pago: ${reg.pagoTxt}`;

        if(reg.tipo === 'Gasto') {
            const egc = document.getElementById('edit-gasto-concepto'); if(egc) reg.servicio = egc.value;
            const egm = document.getElementById('edit-gasto-monto'); if(egm) reg.monto = parseFloat(egm.value) || 0;
        } else {
            const eb = document.getElementById('edit-barbero'); if(eb) reg.barbero = eb.value;
            reg.servicio = editServiciosActuales.join(' + ') || 'Ninguno';
            const ebed = document.getElementById('edit-bebida'); if(ebed) reg.bebida = ebed.value || '-';
            const em = document.getElementById('edit-monto'); if(em) reg.monto = parseFloat(em.value) || 0;
            const ep = document.getElementById('edit-propina'); if(ep) reg.propina = parseFloat(ep.value) || 0;
            const epago = document.getElementById('edit-pago'); if(epago) reg.pagoTxt = epago.value;
            reg.valEfectivo = reg.pagoTxt === 'Efectivo' ? reg.monto : (reg.pagoTxt === 'Mixto' ? (parseFloat(document.getElementById('edit-monto-efectivo-mixto')?.value)||0) : 0);
            reg.valTarjeta = reg.pagoTxt === 'Tarjeta' ? reg.monto : (reg.pagoTxt === 'Mixto' ? Math.max(0, reg.monto - reg.valEfectivo) : 0);
        }
        reg.editado = true;
        
        let newStr = reg.tipo === 'Gasto' 
            ? `Gasto: ${reg.servicio} | $${reg.monto}` 
            : `${reg.barbero} | $${reg.monto} | Pago: ${reg.pagoTxt}`;

        historialEdiciones.unshift({
            id: Date.now(),
            fecha: new Date().toLocaleString('es-MX', {day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit'}),
            ticketInfo: `[${reg.sucursal}] ${reg.fechaCorta} ${reg.hora} - ${reg.tipo === 'Gasto' ? 'Gasto' : 'Ticket'}`,
            antes: oldStr,
            despues: newStr,
            usuario: rolActual === 'admin' ? 'Admin' : reg.sucursal
        });
        
        if (typeof guardarDatos === 'function') guardarDatos();
    }
    window.cerrarModalEditar(); actualizarVistaHoy();
    const vistaRep = document.getElementById('vista-reportes');
    if(vistaRep && !vistaRep.classList.contains('hidden')) actualizarReportes();
});

// ==========================================
// 9. GASTOS Y CORTE DE CAJA
// ==========================================
window.abrirModalGasto = function() { const m = document.getElementById('modal-gasto'); if(m) m.classList.remove('hidden'); };
window.cerrarModalGasto = function() { const m = document.getElementById('modal-gasto'); if(m) { m.classList.add('hidden'); const f = document.getElementById('form-gasto'); if(f) f.reset(); } };

const formGasto = document.getElementById('form-gasto');
if(formGasto) formGasto.addEventListener('submit', e => {
    e.preventDefault();
    const c = document.getElementById('gasto-concepto')?.value || 'Gasto';
    const m = parseFloat(document.getElementById('gasto-monto')?.value) || 0;
    const now = new Date();
    const hoyLocal = new Date(); const tOffset = hoyLocal.getTimezoneOffset()*60000;
    const hoyIso = new Date(hoyLocal-tOffset).toISOString().split('T')[0];
    registros.unshift({ id: Date.now(), fechaObj: now, fechaCorta: hoyIso, hora: now.toLocaleTimeString('es-MX',{hour:'2-digit',minute:'2-digit'}), sucursal: sucursalActual, barbero: '-', servicio: c, bebida: '-', monto: m, propina: 0, pagoTxt: 'Efectivo', valEfectivo: 0, valTarjeta: 0, editado: false, tipo: 'Gasto' });
    window.cerrarModalGasto(); actualizarVistaHoy();
});

window.abrirModalCorteCaja = function() {
    const m = document.getElementById('modal-corte'); if(!m) return;
    const ci = document.getElementById('corte-ingresos-efvo'); if(ci) ci.textContent = formatoDinero.format(window.ingresosEfvoActuales||0);
    const cp = document.getElementById('corte-propinas'); if(cp) cp.textContent = formatoDinero.format(window.totalPropinasDia||0);
    const cpd = document.getElementById('corte-propinas-detalle');
    if(cpd) {
        const pef = window.totalPropinasEfvoDia || 0;
        const ptar = window.totalPropinasTarjDia || 0;
        cpd.textContent = `(💵 ${formatoDinero.format(pef)} efvo • 💳 ${formatoDinero.format(ptar)} tarj)`;
    }
    const cg = document.getElementById('corte-gastos'); if(cg) cg.textContent = formatoDinero.format(window.gastosTotalesActuales||0);
    const ce = document.getElementById('corte-esperado'); if(ce) ce.textContent = formatoDinero.format(window.cajaEfectivoActual||0);
    const cr = document.getElementById('corte-real'); if(cr) cr.value = '';
    const db = document.getElementById('corte-diferencia-box'); if(db) db.classList.add('hidden');
    m.classList.remove('hidden');
};
window.cerrarModalCorteCaja = function() { const m = document.getElementById('modal-corte'); if(m) m.classList.add('hidden'); };

const corteReal = document.getElementById('corte-real');
if(corteReal) corteReal.addEventListener('input', e => {
    const r = parseFloat(e.target.value) || 0;
    const esp = window.cajaEfectivoActual || 0;
    const dif = r - esp;
    const box = document.getElementById('corte-diferencia-box');
    if(!box) return;
    box.classList.remove('hidden','bg-emerald-950','text-emerald-400','border-emerald-800','bg-red-950','text-red-400','border-red-800');
    if(dif === 0) { box.textContent='CAJA CUADRADA'; box.classList.add('bg-emerald-950','text-emerald-400','border-emerald-800'); }
    else if(dif > 0) { box.textContent='SOBRANTE: '+formatoDinero.format(dif); box.classList.add('bg-emerald-950','text-emerald-400','border-emerald-800'); }
    else { box.textContent='FALTANTE: '+formatoDinero.format(Math.abs(dif)); box.classList.add('bg-red-950','text-red-400','border-red-800'); }
});

const formCorte = document.getElementById('form-corte');
if(formCorte) formCorte.addEventListener('submit', e => {
    e.preventDefault();
    const r = parseFloat(document.getElementById('corte-real')?.value) || 0;
    const esp = window.cajaEfectivoActual || 0;
    const dif = r - esp;
    window.cerrarModalCorteCaja();
    const modalExito = document.getElementById('modal-exito');
    if(modalExito) modalExito.classList.remove('hidden');
    let difText = dif===0 ? '✅ CAJA CUADRADA' : (dif>0 ? `⚠️ SOBRANTE: ${formatoDinero.format(dif)}` : `🚨 FALTANTE: ${formatoDinero.format(Math.abs(dif))}`);
    let msg = `💈 CORTE DE CAJA - MB BARBEROS 💈\n📍 Sucursal: ${sucursalActual}\n📅 Fecha: ${new Date().toLocaleDateString('es-MX')}\n\n`;
    msg += `✂️ Tickets: ${window.totalTicketsDia||0}\n💵 Efectivo: ${formatoDinero.format(window.ingresosEfvoActuales||0)}\n💳 Tarjeta: ${formatoDinero.format(window.ingresosTarjetaActuales||0)}\n`;
    msg += `🌟 Propinas: ${formatoDinero.format(window.totalPropinasDia||0)} (${formatoDinero.format(window.totalPropinasEfvoDia||0)} efvo / ${formatoDinero.format(window.totalPropinasTarjDia||0)} tarj)\n`;
    msg += `🚀 TOTAL: ${formatoDinero.format(window.totalIngresosDia||0)}\n💸 Gastos: -${formatoDinero.format(window.gastosTotalesActuales||0)}\n📊 Esperado: ${formatoDinero.format(esp)}\n💰 Contado: ${formatoDinero.format(r)}\n\n${difText}\n\n_BarberOS_`;
    setTimeout(() => {
        if(modalExito) modalExito.classList.add('hidden');
        window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
    }, 2500);
});

// WhatsApp daily summary
window.enviarResumenWhatsApp = function() {
    actualizarVistaHoy();
    const fecha = document.getElementById('filtro-fecha-pos')?.value || new Date().toLocaleDateString('es-MX');
    let msg = `💈 *RESUMEN DEL DÍA - ${sucursalActual}*\n📅 ${fecha}\n\n`;
    msg += `✂️ *Tickets:* ${window.totalTicketsDia||0}\n`;
    msg += `💵 *Efectivo:* ${formatoDinero.format(window.ingresosEfvoActuales||0)}\n`;
    msg += `💳 *Tarjeta:* ${formatoDinero.format(window.ingresosTarjetaActuales||0)}\n`;
    msg += `🌟 *Propinas:* ${formatoDinero.format(window.totalPropinasDia||0)}\n`;
    msg += `🚀 *TOTAL:* ${formatoDinero.format(window.totalIngresosDia||0)}\n`;
    msg += `\n_BarberOS_`;
    window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
};

// ==========================================
// 10. DATOS DE DEMO Y ARRANQUE
// ==========================================
function generarDatosDemo() {
    const barbs = barberosActivos.map(b => b.nombre);
    for(let i=0; i<200; i++) {
        const d = new Date(); d.setDate(d.getDate() - Math.floor(Math.random()*60));
        const propina = Math.random() > 0.5 ? 20 : 0;
        const monto = [220, 380, 120, 330][Math.floor(Math.random()*4)];
        const pago = Math.random() > 0.6 ? 'Tarjeta' : 'Efectivo';
        const valEf = pago === 'Efectivo' ? monto + propina : 0;
        const valTar = pago === 'Tarjeta' ? monto + propina : 0;
        const suc = sucursalesActivas[Math.floor(Math.random()*sucursalesActivas.length)];
        registros.push({
            id: Date.now() + i, fechaObj: d, fechaCorta: d.toISOString().split('T')[0],
            hora: d.toLocaleTimeString('es-MX',{hour:'2-digit',minute:'2-digit'}),
            sucursal: suc, barbero: barbs[Math.floor(Math.random()*barbs.length)],
            servicio: 'Corte de Cabello', bebida: '-', monto, propina, pagoTxt: pago, valEfectivo: valEf, valTarjeta: valTar, editado: false
        });
    }
    registros.sort((a,b) => b.fechaObj - a.fechaObj);
    const ayer = new Date(); ayer.setDate(ayer.getDate()-1);
    pagosNomina.push({ id:1, fechaObj: ayer, fechaStr: ayer.toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric'}), barbero: 'David', monto: 1500, metodo: 'Transferencia' });
}

generarDatosDemo();
renderizarBotonesLogin();


// TEMA CLARO/OSCURO
window.toggleTheme = function() {
    document.documentElement.classList.toggle('light-theme');
    localStorage.setItem('mb_theme', document.documentElement.classList.contains('light-theme') ? 'light' : 'dark');
};
if(localStorage.getItem('mb_theme') === 'light') {
    document.documentElement.classList.add('light-theme');
}
