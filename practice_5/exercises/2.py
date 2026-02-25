import re

s = input()

x = re.search(r"ab{2,3}", s)

if x:
    print(x.group())
else:
    print("No matches")