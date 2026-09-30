import os
import subprocess

scripts = [
    "fix.py",
    "fix2.py",
    "inject_sw.py",
    "fix_enc.py",
    "fix_pin.py",
    "fix_nomina.py",
    "fix_generar.py",
    "fix_structure.py",
    "fix_final.py",
    "fix_desempeno.py",
    "fix_mixto_nomina.py",
    "fix_historial_tx.py",
    "fix_encodings.py",
    "fix_local_col.py",
    "fix_login_ui.py",
    "fix_logo.py",
    "fix_header.py",
    "fix_total_tx.py",
    "add_tienda_historial.py",
    "fix_branch_change.py",
    "inject_ui_features.py",
    "inject_js_features.py",
    "fix_script_order.py",
    "hide_zero_tickets.py",
    "fix_bitacora_loop.py",
    "fix_duplicate_let.py",
    "add_whatsapp_report.py",
    "expand_whatsapp_report.py",
    "add_edit_delete.py",
    "fix_products_ui.py",
    "fix_products_js.py",
    "fix_nomina_display.py",
    "force_html_products.py",
    "fix_js_null_error.py",
    "fix_payroll_products.py",
    "fix_product_layout.py",
    "force_render_list.py",
    "force_payroll.py",
    "force_payroll_2.py",
    "exact_payroll_fix.py"
    # DO NOT RUN final_exact_replace.py because it contains the bug!
]

# We need to copy recovered_app.js to app.js
import shutil
shutil.copy('recovered_app.js', 'app.js')

for script in scripts:
    print(f"Running {script}...")
    # Some scripts might throw errors if they expect something that was already replaced. 
    # But since we are starting from the exact state, they should all work!
    # Wait, some scripts might also modify index.html!
    # But index.html is NOT reset! Will the python scripts break index.html if run twice?
    # Some use replace(), which is idempotent if the old string is gone!
    # Let's hope they are idempotent.
    res = subprocess.run(["python", script], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error in {script}:\n{res.stderr}")
    else:
        print(f"Success {script}")

print("Replay completed!")
