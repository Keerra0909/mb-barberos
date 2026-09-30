c = open('index.html', 'r', encoding='utf-8').read()

# Change login background to pure black to merge perfectly with the logo
c = c.replace(
    '<div id="pantalla-login" class="fixed inset-0 bg-[#050505] z-[100] flex flex-col items-center justify-center p-4">',
    '<div id="pantalla-login" class="fixed inset-0 bg-black z-[100] flex flex-col items-center justify-center p-4">'
)

# And center the text inside the buttons by removing flex/justify-between
js_c = open('app.js', 'r', encoding='utf-8').read()
js_c = js_c.replace(
    'class="w-full bg-[#111] hover:bg-[#1a1a1a] border border-zinc-800 text-zinc-300 p-4 rounded-sm transition-all flex items-center justify-between group"',
    'class="w-full bg-[#111] hover:bg-[#1a1a1a] border border-zinc-800 text-zinc-300 p-4 rounded-sm transition-all text-center group"'
)
# Remove the chevron icon as it's not needed if we are centering text
js_c = js_c.replace(
    '<i class="fa-solid fa-chevron-right text-xs opacity-0 group-hover:opacity-100 transition-opacity text-emerald-500"></i>',
    ''
)

open('index.html', 'w', encoding='utf-8').write(c)
open('app.js', 'w', encoding='utf-8').write(js_c)

# Bump cache to v4
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = sw.replace("CACHE_NAME = 'mb-barberos-v3'", "CACHE_NAME = 'mb-barberos-v4'")
open('sw.js', 'w', encoding='utf-8').write(sw)

# Cache bust index
import time, re
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

print('Login screen centered and logo background fixed.')
