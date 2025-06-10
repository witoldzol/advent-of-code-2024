f = open('input7')
# f = open('testinput')

def calc(numbers, target):
    if len(numbers) == 0:
        return target == 0
    add = target - numbers[-1]
    multi = target//numbers[-1]
    return calc(numbers[:-1], add) or (target%numbers[-1]==0 and calc(numbers[:-1], multi))

sum = 0
for l in f:
    target, input = l.rstrip().split(':')
    inputs = [int(x) for x in input.split(' ') if x]
    target = int(target)
    if calc(inputs, target):
        sum += target

print(sum)
