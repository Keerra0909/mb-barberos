import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Fix 1: iniciarSesion -> Add Todas to the select options
js = js.replace("""        const selSucursal = document.getElementById('sucursal-select');
        if(selSucursal) {
            selSucursal.innerHTML = '';
            [...sucursalesActivas].sort().forEach(s => {
                selSucursal.innerHTML += `<option value="${s}" class="text-black">Sucursal: ${s}</option>`;
            });
            sucursalActual = selSucursal.value;
        }""", """        const selSucursal = document.getElementById('sucursal-select');
        if(selSucursal) {
            selSucursal.innerHTML = '<option value="Todas" class="text-black">Sucursal: Todas</option>';
            [...sucursalesActivas].sort().forEach(s => {
                selSucursal.innerHTML += `<option value="${s}" class="text-black">Sucursal: ${s}</option>`;
            });
            sucursalActual = 'Todas';
        }""")

# Fix 2: actualizarMenuSucursalesHeader -> Add Todas to the select options
js = js.replace("""function actualizarMenuSucursalesHeader() {
    const sel = document.getElementById('sucursal-select');
    if(!sel) return;
    const current = sel.value || sucursalActual;
    sel.innerHTML = '';
    [...sucursalesActivas].sort().forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        if(s === current) opt.selected = true;
        sel.appendChild(opt);
    });
}""", """function actualizarMenuSucursalesHeader() {
    const sel = document.getElementById('sucursal-select');
    if(!sel) return;
    const current = sel.value || sucursalActual;
    sel.innerHTML = '';
    const optTodas = document.createElement('option');
    optTodas.value = 'Todas'; optTodas.textContent = 'Sucursal: Todas';
    if('Todas' === current) optTodas.selected = true;
    sel.appendChild(optTodas);
    [...sucursalesActivas].sort().forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        if(s === current) opt.selected = true;
        sel.appendChild(opt);
    });
}""")

# Fix 3: actualizarSelectsForm -> filter barberos
js = js.replace("""    const barberosLocal = barberosActivos
        .filter(b => rolActual === 'admin' || b.sucursal === sucursalActual)
        .map(b => b.nombre).sort();""", """    const barberosLocal = barberosActivos
        .filter(b => sucursalActual === 'Todas' || b.sucursal === sucursalActual)
        .map(b => b.nombre).sort();""")

# Fix 4: actualizarVistaHoy -> filter by sucursal
js = js.replace("""    let regsHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo !== 'Gasto');
    if(rolActual !== 'admin') regsHoy = regsHoy.filter(r => r.sucursal === sucursalActual);
    let gastosHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo === 'Gasto');
    if(rolActual !== 'admin') gastosHoy = gastosHoy.filter(r => r.sucursal === sucursalActual);""", """    let regsHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo !== 'Gasto');
    if(sucursalActual !== 'Todas') regsHoy = regsHoy.filter(r => r.sucursal === sucursalActual);
    let gastosHoy = registros.filter(r => r.fechaCorta === fechaFiltro && r.tipo === 'Gasto');
    if(sucursalActual !== 'Todas') gastosHoy = gastosHoy.filter(r => r.sucursal === sucursalActual);""")

# Fix 5: actualizarReportes -> filter barberos and records
js = js.replace("""    const regsPeriodo = registros.filter(r => r.tipo !== 'Gasto' && r.fechaObj >= dateDesde && r.fechaObj <= dateHasta);
    const pagosPeriodo = pagosNomina.filter(p => p.fechaObj >= dateDesde && p.fechaObj <= dateHasta);""", """    let regsPeriodo = registros.filter(r => r.tipo !== 'Gasto' && r.fechaObj >= dateDesde && r.fechaObj <= dateHasta);
    if(sucursalActual !== 'Todas') regsPeriodo = regsPeriodo.filter(r => r.sucursal === sucursalActual);
    const pagosPeriodo = pagosNomina.filter(p => p.fechaObj >= dateDesde && p.fechaObj <= dateHasta);""")

js = js.replace("""    // Nómina
    const barberosLocal = barberosActivos.map(b => typeof b === 'string' ? b : b.nombre);""", """    // Nómina
    const barberosLocal = barberosActivos
        .filter(b => sucursalActual === 'Todas' || b.sucursal === sucursalActual)
        .map(b => typeof b === 'string' ? b : b.nombre);""")

open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
