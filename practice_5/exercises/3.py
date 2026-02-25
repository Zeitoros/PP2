import re

s = input()

p = r"[a-z]+_[a-z]+"

x = re.findall(p,s)

if x:
    print(", ".join(x))
else:
    print("No matches")