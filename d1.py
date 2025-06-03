f = open('input1')
left_input = []
right_input = {}

for l in f:
    left, right = l.rstrip().split()
    left_input.append(left)
    if right in right_input:
        right_input[right] = right_input[right] + 1
    else:
        right_input[right] = 1

similarity_score = 0

for l in left_input:
    if l in right_input:
        similarity_score += (int(l) * right_input[l])

print('similarity_score')
print(similarity_score)
