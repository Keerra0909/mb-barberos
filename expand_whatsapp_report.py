import time, re

c = open('app.js', 'r', encoding='utf-8').read()

# 1. Add new variables to actualizarVistaHoy
old_globals = """    // Asignar variables globales para el modal
    window.cajaEfectivoActual = cEf;
    window.gastosTotalesActuales = totalGastos;
    window.ingresosEfvoActuales = cEfBruto;"""

new_globals = """    // Asignar variables globales para el modal y el reporte de WhatsApp
    window.cajaEfectivoActual = cEf;
    window.gastosTotalesActuales = totalGastos;
    window.ingresosEfvoActuales = cEfBruto;
    window.ingresosTarjetaActuales = cTar;
    window.totalIngresosDia = totalIngresos;
    window.totalTicketsDia = regsHoy.filter(r => r.tipo !== 'Gasto').length;
    window.totalPropinasDia = regsHoy.reduce((acc, r) => acc + (r.propina || 0), 0);"""
c = c.replace(old_globals, new_globals)

# 2. Update WhatsApp Message logic
old_msg = """    let msg = `💈 *CORTE DE CAJA - MB BARBEROS* 💈\\n`;
    msg += `📍 *Sucursal:* ${sucursalActual}\\n`;
    msg += `📅 *Fecha:* ${new Date().toLocaleDateString('es-MX')} ${new Date().toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'})}\\n\\n`;
    msg += `💵 *Ingresos Efectivo:* ${formatoDinero.format(window.ingresosEfvoActuales || 0)}\\n`;
    msg += `💸 *Gastos (-):* ${formatoDinero.format(window.gastosTotalesActuales || 0)}\\n`;
    msg += `📊 *Esperado en Cajón:* ${formatoDinero.format(window.cajaEfectivoActual || 0)}\\n`;
    msg += `💰 *Efectivo Real (Contado):* ${formatoDinero.format(r)}\\n\\n`;
    msg += `${difText}\\n\\n`;
    msg += `_Generado desde BarberOS_`;"""

new_msg = """    let msg = `💈 *CORTE DE CAJA - MB BARBEROS* 💈\\n`;
    msg += `📍 *Sucursal:* ${sucursalActual}\\n`;
    msg += `📅 *Fecha:* ${new Date().toLocaleDateString('es-MX')} ${new Date().toLocaleTimeString('es-MX', {hour: '2-digit', minute:'2-digit'})}\\n\\n`;
    
    msg += `📈 *RESUMEN DEL DÍA*\\n`;
    msg += `✂️ *Tickets Cobrados:* ${window.totalTicketsDia || 0}\\n`;
    msg += `💳 *Pagos con Tarjeta:* ${formatoDinero.format(window.ingresosTarjetaActuales || 0)}\\n`;
    msg += `💵 *Pagos en Efectivo:* ${formatoDinero.format(window.ingresosEfvoActuales || 0)}\\n`;
    msg += `🌟 *Propinas Totales:* ${formatoDinero.format(window.totalPropinasDia || 0)}\\n`;
    msg += `🚀 *TOTAL VENTAS:* ${formatoDinero.format(window.totalIngresosDia || 0)}\\n\\n`;
    
    msg += `🔒 *BALANCE DE CAJA (Efectivo)*\\n`;
    msg += `💸 *Gastos Retirados:* -${formatoDinero.format(window.gastosTotalesActuales || 0)}\\n`;
    msg += `📊 *Esperado en Cajón:* ${formatoDinero.format(window.cajaEfectivoActual || 0)}\\n`;
    msg += `💰 *Físico Contado:* ${formatoDinero.format(r)}\\n\\n`;
    
    msg += `${difText}\\n\\n`;
    msg += `_Generado automáticamente por BarberOS_`;"""
c = c.replace(old_msg, new_msg)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("WhatsApp report expanded with daily summary.")
