import time, re

c = open('app.js', 'r', encoding='utf-8').read()

# Fix in actualizarReportes
old_nomina_logic = """    regsPeriodo.forEach(r => {
        // Sueldo = 50% of tickets + 100% of tips. (If they sell a product, right now it splits 50% too. Let's assume that's intended unless requested otherwise).
        const ganancia = (r.monto * 0.5) + r.propina;
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        if(mapNomina[r.barbero]) {
            mapNomina[r.barbero].ventasBrutas += r.monto;
            mapNomina[r.barbero].sueldo += ganancia;
        }
    });"""

new_nomina_logic = """    regsPeriodo.forEach(r => {
        // Sueldo = 50% of services + 100% of tips. Products pay 0% commission.
        let montoProductos = 0;
        const items = r.servicio.split(' + ');
        items.forEach(item => {
            if (productosActivos.includes(item)) {
                montoProductos += (preciosBase[item] || 0);
            }
        });
        
        let montoComisionable = Math.max(0, r.monto - montoProductos);
        const ganancia = (montoComisionable * 0.5) + r.propina;
        
        if(!mapBarberos[r.barbero]) mapBarberos[r.barbero] = 0; 
        mapBarberos[r.barbero] += ganancia; 
        if(mapNomina[r.barbero]) {
            mapNomina[r.barbero].ventasBrutas += r.monto;
            mapNomina[r.barbero].sueldo += ganancia;
        }
    });"""

c = c.replace(old_nomina_logic, new_nomina_logic)

open('app.js', 'w', encoding='utf-8').write(c)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Product commission removed from payroll logic.")
