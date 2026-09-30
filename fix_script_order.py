import re, time

c = open('index.html', 'r', encoding='utf-8').read()

# Extract the script block
script_block = re.search(r'<script src="app\.js\?v=\d+"></script>\s*<script>.*?navigator\.serviceWorker\.register.*?</script>', c, re.DOTALL)

if script_block:
    block_str = script_block.group(0)
    # Remove it from its current position
    c = c.replace(block_str, '')
    # Put it right before </body>
    c = c.replace('</body>', block_str + '\n</body>')
    
    # Cache bust
    c = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', c)
    open('index.html', 'w', encoding='utf-8').write(c)

    sw = open('sw.js', 'r', encoding='utf-8').read()
    sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
    open('sw.js', 'w', encoding='utf-8').write(sw)
    print("Script tags moved to the bottom!")
else:
    print("Could not find script block")
