import time, re

c = open('index.html', 'r', encoding='utf-8').read()

# Reduce logo size to look sharper (h-52 is ~208px, smaller than original 264px so no pixelation)
old_img = 'class="h-[400px] object-contain mix-blend-screen"'
new_img = 'class="h-52 object-contain mix-blend-screen"'
c = c.replace(old_img, new_img)

# Cache bust
c = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', c)
open('index.html', 'w', encoding='utf-8').write(c)

# Update sw.js cache version
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Logo size reduced.")
