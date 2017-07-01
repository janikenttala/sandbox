import sys
import json

events = list()
for line in sys.stdin.readlines():
    line = json.loads(line)
    events.append(line)

print json.dumps(events)