import re
import time

js = open('app.js', 'r', encoding='utf-8').read()

# The error is that the forEach loop is closed with `}` instead of `});`
old_str = "            </tr>`;\n    }\n    \n    if(totVentas > 0 || totSueldo > 0 || totProps > 0 || totPagado > 0) {"
new_str = "            </tr>`;\n    });\n    \n    if(totVentas > 0 || totSueldo > 0 || totProps > 0 || totPagado > 0) {"

if old_str in js:
    js = js.replace(old_str, new_str)
    print("Fixed!")
else:
    print("Could not find the exact string. Trying regex...")
    # fallback
    js = re.sub(r'            </tr>`;\s*}\s*if\(totVentas > 0', r'            </tr>`;\n    });\n    \n    if(totVentas > 0', js)

open('app.js', 'w', encoding='utf-8').write(js)

# Cache bust
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
