import json

# Scan all write_to_file calls for app.js in the transcript and print their timestamps + sizes
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

        for tc in data.get('tool_calls', []):
            if tc.get('name') == 'write_to_file':
                args = tc.get('args', {})
                target = args.get('TargetFile', '')
                if 'app.js' in target:
                    code = args.get('CodeContent', '')
                    results.append((created, len(code)))
                    print(f"{created} -> {len(code)} bytes")

print(f"\nTotal: {len(results)} write_to_file calls for app.js")
