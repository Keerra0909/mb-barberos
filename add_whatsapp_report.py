import time, re

c = open('index.html', 'r', encoding='utf-8').read()

# Inject Success Modal
success_modal = """
    <!-- Modal de Éxito -->
    <div id="modal-exito" class="fixed inset-0 bg-[#050505]/95 backdrop-blur-md z-[60] hidden flex flex-col items-center justify-center p-4 transition-opacity duration-300">
        <div class="w-20 h-20 bg-emerald-500/20 rounded-full flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(16,185,129,0.3)] animate-pulse">
            <i class="fa-solid fa-check text-4xl text-emerald-400"></i>
        </div>
        <h2 class="text-2xl font-sans font-bold text-white tracking-widest uppercase mb-2">¡Corte Registrado!</h2>
        <p class="text-zinc-400 text-center max-w-sm text-sm mb-8">El cajón ha sido cerrado correctamente. Preparando el reporte de WhatsApp para el administrador...</p>
    </div>
"""

if "modal-exito" not in c:
    c = c.replace('</body>', success_modal + '\n</body>')
    
open('index.html', 'w', encoding='utf-8').write(c)

js = open('app.js', 'r', encoding='utf-8').read()

old_submit = """document.getElementById('form-corte').addEventListener('submit', e => {
    e.preventDefault();
    alert('Corte de caja registrado. Se enviará un reporte al administrador.');
    cerrarModalCorteCaja();
});"""

new_submit = """document.getElementById('form-corte').addEventListener('submit', e => {
    e.preventDefault();
    
    const r = parseFloat(document.getElementById('corte-real').value) || 0;
    const esp = window.cajaEfectivoActual || 0;
    const dif = r - esp;
    
    // Ocultar modal de corte y mostrar el modal bonito de éxito
    cerrarModalCorteCaja();
    const modalExito = document.getElementById('modal-exito');
    modalExito.classList.remove('hidden');
    
    // Preparar mensaje de WhatsApp
    let difText = dif === 0 ? '✅ *CAJA CUADRADA*' : (dif > 0 ? `⚠️ *SOBRANTE:* ${formatoDinero.format(dif)}` : `🚨 *FALTANTE:* ${formatoDinero.format(Math.abs(dif))}`);
    
    let msg = `💈 *CORTE DE CAJA - MB BARBEROS* 💈\\n`;
    msg += `📍 *Sucursal:* ${sucursalActual}\\n`;
    msg += `📅 *Fecha:* ${new Date().toLocaleDateString('es-MX')} ${new Date().toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'})}\\n\\n`;
    msg += `💵 *Ingresos Efectivo:* ${formatoDinero.format(window.ingresosEfvoActuales || 0)}\\n`;
    msg += `💸 *Gastos (-):* ${formatoDinero.format(window.gastosTotalesActuales || 0)}\\n`;
    msg += `📊 *Esperado en Cajón:* ${formatoDinero.format(window.cajaEfectivoActual || 0)}\\n`;
    msg += `💰 *Efectivo Real (Contado):* ${formatoDinero.format(r)}\\n\\n`;
    msg += `${difText}\\n\\n`;
    msg += `_Generado desde BarberOS_`;
    
    // Abrir WhatsApp y quitar el modal de éxito después de 2.5 segundos
    setTimeout(() => {
        modalExito.classList.add('hidden');
        const url = `https://wa.me/?text=${encodeURIComponent(msg)}`;
        window.open(url, '_blank');
        
        // Aquí normalmente limpiaríamos la bitácora o la marcaríamos como cerrada.
    }, 2500);
});"""

js = js.replace(old_submit, new_submit)
open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("WhatsApp integration and native success modal added.")
