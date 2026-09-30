c = open('index.html', 'r', encoding='utf-8').read()

# Fix the PIN placeholder - find and replace any corrupted placeholder on pin-input
import re

# Replace whatever broken placeholder is there with simple dots
c = re.sub(
    r'(<input[^>]*id="pin-input"[^>]*placeholder=")[^"]*(")',
    r'\g<1>· · · ·\g<2>',
    c
)

open('index.html', 'w', encoding='utf-8').write(c)
print('done')
