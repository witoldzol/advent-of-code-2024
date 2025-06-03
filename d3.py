import re

f = open('input3')
sum = 0
for l in f:
    m = re.findall(r"mul\((\d{0,3}),(\d{0,3})\)", l)
    for x,y in m:
        sum += int(x) * int(y)
print('sum')
print(sum)


