import json
import sys

runs = json.load(sys.stdin)
pending = [r for r in runs if str(r.get('status', '')).lower() != 'completed']
print(len(pending))
