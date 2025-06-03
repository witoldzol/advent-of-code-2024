import re

f = open('input3')
sum = 0
do = True
for l in f:
    matches = re.findall(r"(mul)\((\d{0,3}),(\d{0,3})\)|(do)\(\)|(don't)\(\)", l)
    for m in matches:
        if m[0] and m[0] == 'mul':
            if do:
                sum += int(m[1]) * int(m[2])
        elif m[3]:
            do = True
        elif m[4]:
            do = False
print(sum)
