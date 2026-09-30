import json, shutil, re, time

# Find the last write_to_file for app.js before 16:30 UTC (11:30 CST)
# That's the 2026-09-28T22:37:06Z write = 35730 bytes (last clean write before all the patching)
# Then we replay the scripts up to fix_nomina_display.py

# Step 1: extract app.js at 22:37:06Z (the last full clean write)
best_code = None
best_time = None

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
        if created != "2026-09-28T22:37:06Z":
            continue
        for tc in data.get('tool_calls', []):
            if tc.get('name') == 'write_to_file':
                args = tc.get('args', {})
                if 'app.js' in args.get('TargetFile', ''):
                    best_code = args.get('CodeContent', '')
                    best_time = created
                    print(f"Found base app.js at {created}: {len(best_code)} bytes")

if best_code:
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(best_code)
    print("Base app.js written.")
else:
    print("ERROR: Could not find base app.js!")
    exit(1)
