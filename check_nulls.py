import re, time

js = open('app.js', 'r', encoding='utf-8').read()

# Fix all top-level document.getElementById calls at line level that don't have null checks
# Pattern: const X = document.getElementById('Y'); X.something = ...
# Replace with: const X = document.getElementById('Y'); if(X) X.something = ...

# Also fix: document.getElementById('X').addEventListener -> safe version
# We already did addEventListener. Let's also fix direct property sets at module level.

# Specific known patterns that crash:
# 1. renderizarListaModal already fixed
# 2. actualizarTodasLasListas calls - safe since renderizarListaModal now guards
# 3. actualizarSelectsForm - accesses barbero, servicio, bebida which exist in HTML

# Let's also check for any .innerHTML = or .textContent = or .value = at TOP LEVEL
# (not inside functions)

# The safest fix: wrap actualizarTodasLasListas call at startup
# Currently it calls renderizarListaModal('lista-sucursales-modal',...) etc.
# If the modal doesn't exist in the DOM yet - it returns now due to our fix.
# The real issue: actualizarSelectsForm() which does:
# sBarbero.innerHTML = ... on elements that DO exist
# Let's check if selectsForm is guarded

print(js[js.find('function actualizarSelectsForm'):js.find('function actualizarSelectsForm')+500])
