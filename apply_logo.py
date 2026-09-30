c = open('index.html', 'r', encoding='utf-8').read()

# Replace logo.png with logo_cropped.png
c = c.replace('src="logo.png"', 'src="logo_cropped.png"')

# Bump index cache again
import time, re
c = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', c)
open('index.html', 'w', encoding='utf-8').write(c)

# Update sw.js
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = sw.replace('./logo.png', './logo_cropped.png')
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)

print("Updated to use centered logo!")
