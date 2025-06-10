f = open('input7')
# f = open('testinput')

def calc(numbers, target, sum):
    if not numbers:
        return target == sum 
    add = sum + numbers[0]
    if sum == 0:
        multi = numbers[0]
        concat = numbers[0]
    else:
        multi = sum * numbers[0]
        concat = int(str(sum) + str(numbers[0]))
    return calc(numbers[1:], target, add) or calc(numbers[1:], target, multi) or calc(numbers[1:], target, concat)

sum = 0
for l in f:
    target, input = l.rstrip().split(':')
    inputs = [int(x) for x in input.split(' ') if x]
    target = int(target)
    res = calc(inputs, target, 0)
    if res:
        sum += target

print(sum)
