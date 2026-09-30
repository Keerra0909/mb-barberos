import json
import sys

with open('recovery.json', 'r', encoding='utf-16') as f:
    # Powershell Out-File uses utf-16 by default!
    line = f.read().strip()
    
# It's a JSON line
try:
    data = json.loads(line)
except Exception as e:
    print(f"Failed to parse JSON: {e}")
    sys.exit(1)

# Find the tool call for write_to_file
found = False
for tc in data.get('tool_calls', []):
    if tc.get('name') == 'write_to_file':
        args = tc.get('args', {})
        target = args.get('TargetFile', '')
        if 'app.js' in target:
            code = args.get('CodeContent', '')
            with open('recovered_app.js', 'w', encoding='utf-8') as out:
                out.write(code)
            print(f"Recovered {len(code)} bytes to recovered_app.js!")
            found = True
            break
            
if not found:
    print("Could not find the write_to_file tool call in the JSON line.")
