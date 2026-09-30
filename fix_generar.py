c = open('app.js','r',encoding='utf-8').read()

extra = """
// Auto-set POS date to today
const fechaPosInput = document.getElementById('filtro-fecha-pos');
if(fechaPosInput) fechaPosInput.value = new Date().toISOString().split('T')[0];

// GENERAR button for reports
const btnFiltrar = document.getElementById('btn-filtrar-reportes');
if(btnFiltrar) btnFiltrar.addEventListener('click', () => actualizarReportes());
"""

if 'btn-filtrar-reportes' not in c:
    c = c.rstrip() + extra
    open('app.js','w',encoding='utf-8').write(c)
    print('done')
else:
    print('already exists')
