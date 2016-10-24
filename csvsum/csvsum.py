import sys

total = 0
for line in sys.stdin.readlines():
    payment = float(line.rstrip().split("\t")[1].replace(",", "."))
    total += payment

print total
