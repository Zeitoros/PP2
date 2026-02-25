import re

s = input()

p = r"[ ,.]"

x = re.sub(p, ":", s)

print(x)