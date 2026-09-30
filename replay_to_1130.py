import subprocess, re, time, shutil

# Also restore index.html to its state at ~11:30 AM
# First let's find it in the transcript
import json

best_html = None
best_html_time = None

with open(r'C:\Users\nzakh\.gemini\antigravity\brain\a1e76109-c654-4b08-a4e1-e8fa1c3b7308\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except:
            continue
        created = data.get('created_at', '')
        # Find index.html writes before 16:30 UTC (11:30 CST)
        if created < "2026-09-29T16:00" or created > "2026-09-29T16:32":
            continue
        for tc in data.get('tool_calls', []):
            if tc.get('name') == 'write_to_file':
                args = tc.get('args', {})
                target = args.get('TargetFile', '')
                if 'index.html' in target:
                    code = args.get('CodeContent', '')
                    if len(code) > 100:
                        best_html = code
                        best_html_time = created
                        print(f"Found index.html at {created}: {len(code)} bytes")

if best_html:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(best_html)
    print(f"index.html restored from {best_html_time}")
else:
    print("No index.html write found in that window - keeping current")

# Now run the scripts that were executed from the base state up to 11:30 AM (16:31 UTC)
scripts_to_run = [
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
]

for script in scripts_to_run:
    result = subprocess.run(['python', script], capture_output=True, text=True, encoding='utf-8', errors='replace')
    status = "OK" if result.returncode == 0 else "FAIL"
    err = result.stderr.strip()[:100] if result.stderr else ''
    print(f"{status}: {script} {err}")

# Bump cache
idx = open('index.html', 'r', encoding='utf-8').read()
idx = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', idx)
open('index.html', 'w', encoding='utf-8').write(idx)

sw = open('sw.js', 'r', encoding='utf-8').read()
sw = re.sub(r"CACHE_NAME = 'mb-barberos-v\d+'", f"CACHE_NAME = 'mb-barberos-v{int(time.time())}'", sw)
open('sw.js', 'w', encoding='utf-8').write(sw)
print("\nDone. Cache busted.")
