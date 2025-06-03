f = open('input1')
left_input = []
right_input = []

for l in f:
    left, right = l.rstrip().split()
    left_input.append(left)
    right_input.append(right)

left_input_sorted = sorted(left_input)
right_input_sorted = sorted(right_input)

sum_of_diff = 0

for i in range(1000):
    sum_of_diff += abs(int(left_input_sorted[i]) - int(right_input_sorted[i]))

print('solution:')
print(sum_of_diff)
