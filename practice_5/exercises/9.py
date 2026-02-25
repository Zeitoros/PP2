import re

s = input()

p = re.sub(r"(?=[A-Z])", " ", s).strip()

print(p)