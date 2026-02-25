import re

s = input()

x = re.search(r"ab*", s)

if x:
    print(x.group())
else:
    print("No matches")