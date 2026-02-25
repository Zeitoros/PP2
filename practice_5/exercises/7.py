import re

snake = input()

x = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), snake)

print(x[0].upper() + x[1:] if x else "")