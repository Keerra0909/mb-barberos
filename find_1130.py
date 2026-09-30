import json
import sys
import os

# We need to find write_to_file calls for app.js around 11:25-11:32 AM CST (16:25-16:32 UTC)
# on 2026-09-29

target_start = "2026-09-29T16:25"
target_end = "2026-09-29T16:35"

results = []

with open(r'C:\Users\nzakh\.gemini\antigravity\brain\a1e76109-c654-4b08-a4e1-e8fa1c3b7308\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except:
            continue

        created = data.get('created_at', '')
        if not (created >= target_start and created <= target_end):
            continue

        # Look for tool_calls with write_to_file to app.js
        for tc in data.get('tool_calls', []):
            if tc.get('name') == 'write_to_file':
                args = tc.get('args', {})
                target = args.get('TargetFile', '')
                if 'app.js' in target:
                    code = args.get('CodeContent', '')
                    results.append((created, len(code), code))
                    print(f"Found write_to_file to app.js at {created}, size={len(code)}")

# Save the largest one to see which is more complete
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    best = results[0]
    print(f"\nBest match: {best[0]} ({best[1]} bytes)")
    with open('app_at_1130.js', 'w', encoding='utf-8') as f:
        f.write(best[2])
    print("Saved to app_at_1130.js")
else:
    print("No results found!")
    # Try wider window
    print("Trying wider window...")
