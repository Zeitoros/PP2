import re

s = input()

p = list(filter(None, re.split(r"(?=[A-Z])", s)))

print(p)