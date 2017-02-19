# convert speedtest logs to plottable numbers

# Example format:
# 2017/01/02/03-11-19-lte800.log:Download: 22.43 Mbit/s

import sys
import re
i = 0

print "date-time, Mbit/s"
for line in sys.stdin.readlines():
    line = line.rstrip()
    matches = re.findall("(\d+)/(\d+)/(\d+)/(\d+)-(\d+)-(\d+).*?(\S+) Mbit/s",
                         line)

    for match in matches:
        (y, m, d, h, m, s, speed) = match
        print "%s-%s-%s %s:%s:%s, %s " % match
