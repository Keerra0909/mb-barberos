import re, time

js = open('app.js', 'r', encoding='utf-8').read()
idx = open('index.html', 'r', encoding='utf-8').read()

# Map old IDs (what app.js uses) -> new IDs (what index.html actually has)
id_map = {
    'app-principal': 'main-app',
}

for old, new in id_map.items():
    count = js.count(f"'{old}'") + js.count(f'"{old}"')
    js = js.replace(f"'{old}'", f"'{new}'")
    js = js.replace(f'"{old}"', f'"{new}"')
    print(f"Replaced '{old}' -> '{new}': {count} occurrences")

open('app.js', 'w', encoding='utf-8') .write(js)

# Cache bust
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)
sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("Done")
