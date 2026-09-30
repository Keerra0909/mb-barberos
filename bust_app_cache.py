c = open('index.html', 'r', encoding='utf-8').read()
import time
ts = int(time.time())
c = c.replace('<script src="app.js?v=4"></script>', f'<script src="app.js?v={ts}"></script>')
open('index.html', 'w', encoding='utf-8').write(c)
print('Done cache bust index.')
