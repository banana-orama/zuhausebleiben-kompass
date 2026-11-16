import json
import sys

for r in json.load(sys.stdin):
    print(r.get('databaseId'), r.get('status'), r.get('conclusion'))
