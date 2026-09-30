import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Fix in iniciarSesion
js = js.replace("""<option value="Todas" class="text-black">Sucursal: Todas</option>""", """<option value="Todas" class="bg-zinc-900 text-zinc-300">Sucursal: Todas</option>""")
js = js.replace("""<option value="${s}" class="text-black">Sucursal: ${s}</option>""", """<option value="${s}" class="bg-zinc-900 text-zinc-300">Sucursal: ${s}</option>""")

# Fix in actualizarMenuSucursalesHeader
js = js.replace("""    const optTodas = document.createElement('option');
    optTodas.value = 'Todas'; optTodas.textContent = 'Sucursal: Todas';
    if('Todas' === current) optTodas.selected = true;""", """    const optTodas = document.createElement('option');
    optTodas.value = 'Todas'; optTodas.textContent = 'Sucursal: Todas';
    optTodas.className = 'bg-zinc-900 text-zinc-300';
    if('Todas' === current) optTodas.selected = true;""")

js = js.replace("""        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        if(s === current) opt.selected = true;""", """        const opt = document.createElement('option');
        opt.value = s; opt.textContent = 'Sucursal: ' + s;
        opt.className = 'bg-zinc-900 text-zinc-300';
        if(s === current) opt.selected = true;""")

open('app.js', 'w', encoding='utf-8').write(js)

# Bust cache
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
open('index.html', 'w', encoding='utf-8').write(html)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
