import re

s = input()

p = re.sub(r"([A-Z])", r"_\1", s).lower()

print(p.lstrip("_"))