import sys

# 1. Update app.js
c = open('app.js','r',encoding='utf-8').read()
c = c.replace("'view-pos'", "'vista-pos'")
c = c.replace("'view-reportes'", "'vista-reportes'")
open('app.js','w',encoding='utf-8').write(c)

# 2. Update index.html
c = open('index.html','r',encoding='utf-8').read()

old_login_logo = """<div class="text-6xl font-sans font-bold silver-text tracking-widest flex items-center justify-center gap-4 mb-4">
                <span class="text-3xl font-light opacity-50">-</span> MB <span class="text-3xl font-light opacity-50">-</span>
            </div>"""
new_login_logo = """<div class="flex items-center justify-center mb-4">
                <img src="logo.png" alt="MB BarberOS" class="h-48 object-contain drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
            </div>"""
c = c.replace(old_login_logo, new_login_logo)

old_header_logo = """<div class="font-sans font-bold silver-text text-2xl font-bold tracking-widest">MB</div>"""
new_header_logo = """<img src="logo.png" alt="MB" class="h-12 object-contain drop-shadow-[0_0_10px_rgba(255,255,255,0.1)]">"""
c = c.replace(old_header_logo, new_header_logo)

c = c.replace('<select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm" required></select>', '<select id="servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>')
c = c.replace('<select id="edit-servicio" class="w-full input-dark rounded-sm p-3 text-sm" required></select>', '<select id="edit-servicio" class="w-full input-dark rounded-sm p-3 text-sm"></select>')

open('index.html','w',encoding='utf-8').write(c)
print("done")
