c = open('app.js', 'r', encoding='utf-8').read()

# Find the exact function signature
old_open = "window.abrirModalPago = function(barbero, saldoPendiente) {"
new_open = """window.toggleMixtoNomina = function(val) {
    const panel = document.getElementById('panel-mixto-nomina');
    if(!panel) return;
    if(val === 'Mixto') {
        panel.classList.remove('hidden');
        calcularTransferenciaNomina();
    } else {
        panel.classList.add('hidden');
    }
}

window.calcularTransferenciaNomina = function() {
    const monto = parseFloat(document.getElementById('pago-monto').value) || 0;
    const ef = parseFloat(document.getElementById('pago-efectivo-mixto').value) || 0;
    const transferencia = Math.max(0, monto - ef);
    document.getElementById('pago-transferencia-mixto').value = transferencia.toFixed(2);
}

window.abrirModalPago = function(barbero, saldoPendiente) {"""

c = c.replace(old_open, new_open, 1)

# Reset the mixto panel when opening modal
old_reset = "document.getElementById('pago-monto').value = saldoPendiente;"
new_reset = """document.getElementById('pago-monto').value = saldoPendiente;
    document.getElementById('pago-metodo').value = 'Efectivo';
    document.getElementById('panel-mixto-nomina').classList.add('hidden');
    document.getElementById('pago-efectivo-mixto').value = 0;
    document.getElementById('pago-transferencia-mixto').value = 0;"""

c = c.replace(old_reset, new_reset, 1)

open('app.js', 'w', encoding='utf-8').write(c)
print('done')
print('toggleMixtoNomina defined:', 'toggleMixtoNomina' in c)
print('calcularTransferenciaNomina defined:', 'calcularTransferenciaNomina' in c)
