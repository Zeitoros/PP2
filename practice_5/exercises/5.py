import re

s = input()

p = r"a.*b"

x = re.search(p,s)

if x:
    print(x.group())
else:
    print("No matches")