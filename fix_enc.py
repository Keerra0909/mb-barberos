c = open('index.html', 'r', encoding='utf-8').read()

# Fix encoding
replacements = [
    ('OPERACIÃ³N', 'OPERACIÓN'),
    ('OperaciÃ³n', 'Operación'),
    ('BORRAR DÃA', 'BORRAR DÍA'),
    ('Borrar DAa', 'Borrar Día'),
    ('Borrar DA-a', 'Borrar Día'),
    ('BORRAR DA\xc3\xada', 'BORRAR DÍA'),
    ('BitA-cora', 'Bitácora'),
    ('BitÃ¡cora', 'Bitácora'),
    ('Bit\u00e1cora', 'Bitácora'),
    ('BITÃ\x81CORA', 'BITÁCORA'),
    ('Filtro R\ufffdpido', 'Filtro Rápido'),
    ('Filtro R\xc3\xa1pido', 'Filtro Rápido'),
    ('sesiA3n', 'sesión'),
    ('sesiÃ³n', 'sesión'),
    ('especA-fico', 'específico'),
    ('especÃ\xadfico', 'específico'),
]

for old, new in replacements:
    c = c.replace(old, new)

open('index.html', 'w', encoding='utf-8').write(c)
print('done')
