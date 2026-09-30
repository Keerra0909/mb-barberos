import re

c = open('index.html', 'r', encoding='utf-8').read()

# Fix: The nomina table was inserted inside the historial section by the previous fix.
# We need to:
# 1. Remove tabla-nomina-barberos from inside the historial section
# 2. Put the full nomina table inside the nomina panel's empty overflow-x-auto div

# Step 1: Remove the misplaced nomina table from the historial section
# It looks like this inside the historial overflow-x-auto:
old_misplaced = '''                          <div class="overflow-x-auto max-h-64">
                              <table class="w-full text-center text-[11px]">
                                  <thead class="bg-[#050505] text-zinc-600 text-[11px] uppercase tracking-widest sticky top-0 border-b border-zinc-800">
                                      <tr><th class="p-3 font-normal text-left pl-6">Fecha</th><th class="p-3 font-normal">Barbero</th><th class="p-3 font-normal">Monto</th><th class="p-3 font-normal text-right pr-6">M\ufffdtodo</th></tr>
                                  </thead>
                                 <tbody id="tabla-nomina-barberos" class="divide-y divide-zinc-900"></tbody>
                                  </table>
                              </div>
  
                             <!-- historial pagos -->
                              <table class="w-full text-left text-xs">
                                 <tbody id="tabla-historial-pagos" class="divide-y divide-zinc-900"></tbody>
                              </table>
                          </div>'''

new_historial = '''                          <div class="overflow-x-auto max-h-64">
                              <table class="w-full text-center text-[11px]">
                                  <thead class="bg-[#050505] text-zinc-600 text-[11px] uppercase tracking-widest sticky top-0 border-b border-zinc-800">
                                      <tr><th class="p-3 font-normal text-left pl-6">Fecha</th><th class="p-3 font-normal">Barbero</th><th class="p-3 font-normal">Monto</th><th class="p-3 font-normal text-right pr-6">Método</th></tr>
                                  </thead>
                                  <tbody id="tabla-historial-pagos" class="divide-y divide-zinc-900"></tbody>
                              </table>
                          </div>'''

if 'tabla-nomina-barberos' in c and 'tabla-historial-pagos' in c:
    # Use regex to find and fix the historial section
    c = re.sub(
        r'<div class="overflow-x-auto max-h-64">.*?</div>\s*</div>\s*</div>',
        new_historial + '\n                          </div>\n                      </div>',
        c,
        flags=re.DOTALL,
        count=1
    )

# Step 2: Fix the empty nomina div - insert full table
old_nomina_empty = '<div class="overflow-x-auto">\n                          </div>'
new_nomina_table = '''<div class="overflow-x-auto">
                              <table class="w-full text-left text-[11px]">
                                  <thead class="bg-[#050505] text-zinc-600 text-[11px] uppercase tracking-widest sticky top-0 border-b border-zinc-800">
                                      <tr>
                                          <th class="p-4 font-normal text-left">Barbero</th>
                                          <th class="p-4 font-normal text-center border-l border-zinc-900">Generado</th>
                                          <th class="p-4 font-normal text-center border-l border-zinc-900">Abonado</th>
                                          <th class="p-4 font-normal text-right border-l border-zinc-900">Saldo</th>
                                          <th class="p-4 font-normal text-center border-l border-zinc-900">Acción</th>
                                      </tr>
                                  </thead>
                                  <tbody id="tabla-nomina-barberos" class="divide-y divide-zinc-900"></tbody>
                              </table>
                          </div>'''

c = c.replace(old_nomina_empty, new_nomina_table, 1)

# Fix encoding issues still present
enc_fixes = [
    ('CORTESÃA', 'CORTESÍA'),
    ('CortesÃa', 'Cortesía'),
    ('CORTESÃ\x81A', 'CORTESÍA'),
    ('Control de N\ufffdmina', 'Control de Nómina'),
    ('Historial de TransAcci\ufffdnes', 'Historial de Transacciones'),
    ('M\ufffdtodo', 'Método'),
    ('BORRAR D\ufffdA', 'BORRAR DÍA'),
    ('Borrar D\ufffdA', 'Borrar Día'),
    ('Bit\ufffdcora', 'Bitácora'),
    ('CORTESA\xc3\x83A', 'CORTESÍA'),
]
for old, new in enc_fixes:
    c = c.replace(old, new)

open('index.html', 'w', encoding='utf-8').write(c)
print('done')
print('tabla-nomina-barberos count:', c.count('tabla-nomina-barberos'))
print('tabla-historial-pagos count:', c.count('tabla-historial-pagos'))
