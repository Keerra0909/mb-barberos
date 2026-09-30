import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Fix 1: Add toggleMixtoNomina and calcularTransferenciaNomina
new_funcs = """window.toggleMixtoNomina = function(val) {
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
};"""

js = js.replace("""window.abrirModalLiquidacion = function(barbero, saldo) { abrirModalPago(barbero, Math.max(0, saldo)); };""", new_funcs + "\n\n" + """window.abrirModalLiquidacion = function(barbero, saldo) { abrirModalPago(barbero, Math.max(0, saldo)); };""")

# Fix 2: Update form-pago-barbero submit
old_submit = """const formPago = document.getElementById('form-pago-barbero');
if(formPago) formPago.addEventListener('submit', e => {
    e.preventDefault();
    const now = new Date();
    const barbero = document.getElementById('pago-barbero-nombre')?.value;
    const monto = parseFloat(document.getElementById('pago-monto')?.value) || 0;
    const metodo = document.getElementById('pago-metodo')?.value || 'Efectivo';
    const hastaStr = document.getElementById('reporte-hasta')?.value || now.toISOString().split('T')[0];
    const fechaPago = new Date(hastaStr + 'T12:00:00');
    pagosNomina.unshift({ id: Date.now(), fechaObj: fechaPago, fechaStr: fechaPago.toLocaleString('es-MX',{day:'2-digit',month:'2-digit',year:'numeric'}), barbero, monto, metodo });
    window.cerrarModalPago();
    actualizarReportes();
});"""

new_submit = """const formPago = document.getElementById('form-pago-barbero');
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
    
    window.cerrarModalPago();
    actualizarReportes();
});"""

js = js.replace(old_submit, new_submit)
open('app.js', 'w', encoding='utf-8').write(js)

# Fix 3: Also attach calcularTransferenciaNomina to pago-monto
js = open('app.js', 'r', encoding='utf-8').read()
old_abrir = """const bm = document.getElementById('pago-monto'); if(bm) bm.value = saldoPendiente;"""
new_abrir = """const bm = document.getElementById('pago-monto'); if(bm) { bm.value = saldoPendiente; bm.addEventListener('input', calcularTransferenciaNomina); }"""
js = js.replace(old_abrir, new_abrir)
open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
