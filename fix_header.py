import time, re

# Update HTML
c = open('index.html', 'r', encoding='utf-8').read()

old_html = """                <div id="contenedor-sucursal" class="border border-zinc-700 bg-black rounded-sm px-3 py-1.5 flex items-center">
                    <select id="sucursal-select" class="bg-transparent text-zinc-300 text-xs uppercase tracking-widest focus:outline-none cursor-pointer">"""

new_html = """                <!-- Fixed title for non-admin branches -->
                <h2 id="titulo-sucursal-fija" class="hidden text-xl md:text-2xl font-bold font-sans text-emerald-500 tracking-widest uppercase mr-4 drop-shadow-[0_0_8px_rgba(16,185,129,0.2)]"></h2>
                
                <div id="contenedor-sucursal" class="border border-zinc-700 bg-black rounded-sm px-3 py-1.5 flex items-center">
                    <select id="sucursal-select" class="bg-transparent text-zinc-300 text-xs uppercase tracking-widest focus:outline-none cursor-pointer">"""

c = c.replace(old_html, new_html)

# Update App.js
js = open('app.js', 'r', encoding='utf-8').read()

old_js = """        const selectHeader = document.getElementById('sucursal-select');
        if(selectHeader) {
            selectHeader.disabled = !esAdmin;
            if(!esAdmin) selectHeader.classList.add('opacity-50');
            else selectHeader.classList.remove('opacity-50');
        }"""

new_js = """        const selectHeader = document.getElementById('sucursal-select');
        const contSucursal = document.getElementById('contenedor-sucursal');
        const tituloFijo = document.getElementById('titulo-sucursal-fija');
        
        if(esAdmin) {
            if(contSucursal) contSucursal.classList.remove('hidden');
            if(selectHeader) selectHeader.disabled = false;
            if(tituloFijo) tituloFijo.classList.add('hidden');
        } else {
            if(contSucursal) contSucursal.classList.add('hidden');
            if(tituloFijo) {
                tituloFijo.classList.remove('hidden');
                tituloFijo.textContent = sucursalIntentada;
            }
        }"""

js = js.replace(old_js, new_js)
open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
c = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', c)
open('index.html', 'w', encoding='utf-8').write(c)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Header logic updated!")
