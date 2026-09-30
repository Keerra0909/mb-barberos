import re

js = open('app.js', 'r', encoding='utf-8').read()
html = open('index.html', 'r', encoding='utf-8').read()

# Find all IDs referenced in app.js
js_ids = set(re.findall(r"getElementById\('([^']+)'\)", js))
js_ids |= set(re.findall(r'getElementById\("([^"]+)"\)', js))

# Find all IDs defined in index.html
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))

missing = js_ids - html_ids
print(f"IDs referenced in app.js but NOT in index.html ({len(missing)}):")
for m in sorted(missing):
    print(f"  MISSING: {m}")

print(f"\nTotal JS IDs: {len(js_ids)}, HTML IDs: {len(html_ids)}")
