c = open('sw.js', 'r', encoding='utf-8').read()
c = c.replace("CACHE_NAME = 'mb-barberos-v1'", "CACHE_NAME = 'mb-barberos-v2'")
open('sw.js', 'w', encoding='utf-8').write(c)
print('Cache invalidated.')
