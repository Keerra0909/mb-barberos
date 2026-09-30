c = open('app.js', 'r', encoding='utf-8').read()

old = "e.preventDefault();\n    if(sucursalActual === 'Todas') { alert('Selecciona una sucursal en espec\ufffd\xadfico arriba.'); return; }\n    \n    const sBarbero"

new = """e.preventDefault();
    if(sucursalActual === 'Todas') { alert('Selecciona una sucursal específica arriba.'); return; }
    if(serviciosActuales.length === 0) { 
        const cont = document.getElementById('servicios-seleccionados');
        cont.classList.remove('hidden');
        cont.innerHTML = '<span class=\"text-red-400 text-xs uppercase tracking-widest py-1\">⚠ Agrega al menos un servicio con el botón +</span>';
        setTimeout(() => { if(serviciosActuales.length === 0) { cont.innerHTML = ''; cont.classList.add('hidden'); } }, 2500);
        return; 
    }
    \n    const sBarbero"""

c = c.replace(old, new, 1)
open('app.js', 'w', encoding='utf-8').write(c)
print('done')
print('serviciosActuales.length check added:', 'serviciosActuales.length === 0' in c)
