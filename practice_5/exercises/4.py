import re

s = input()

p = r"[A-Z][a-z]+"

iter = re.finditer(p,s)

for x in iter:
    print(f"'{x.group()}' on {x.start()}")