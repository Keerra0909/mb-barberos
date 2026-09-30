import re
import time

js = open('app.js', 'r', encoding='utf-8').read()

js = js.replace('            </tr>`;\n    });', '            </tr>`;\n    }')

open('app.js', 'w', encoding='utf-8').write(js)

idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("Syntax fixed")
