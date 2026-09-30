c = open('index.html', 'r', encoding='utf-8').read()

manifest_link = '<link rel="manifest" href="manifest.json">'
if manifest_link not in c:
    c = c.replace('</head>', manifest_link + '\n</head>', 1)

sw_reg = '<script>\nif ("serviceWorker" in navigator) {\n    navigator.serviceWorker.register("./sw.js")\n        .then(() => console.log("MB BarberOS: Offline listo."))\n        .catch(e => console.error("SW:", e));\n}\n</script>'

if 'serviceWorker' not in c:
    c = c.replace('</body>', sw_reg + '\n</body>', 1)

open('index.html', 'w', encoding='utf-8').write(c)
print('done')
