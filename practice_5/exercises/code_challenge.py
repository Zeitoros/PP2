import re

txt = "The rain in Spain"

x = re.search("Spain", txt)

if x:
    print(x.span())