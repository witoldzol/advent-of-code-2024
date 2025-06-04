f = open('./input5')
def is_correct_order(rules: dict[str,set[str]], input: list[str]) -> int:
    for idx, x in enumerate(input):
        if x in rules:
            rule: set[str] = rules[x]
            # check all elements before the x, if they make run invalid
            for y in range(idx):
                #print(f'is {y} in {rule}?')
                if input[y] in rule:
                    return 0
    #print('in order:\n', input)
    mid = len(input) // 2
    #print('mid', mid)
    #print('mid val', int(input[mid]))
    return  int(input[mid])

page_rules = {}
sum = 0
is_rules = True
for l in f:
    if l == '\n':
        #print('end of page rules')
        is_rules = False
        continue
    if is_rules: 
        before, after = l.rstrip().split('|')
        if before in page_rules:
            page_rules[before].add(after)
        else:
            page_rules[before] = {after}
    else:
        input = l.rstrip().split(',')
        sum += is_correct_order(page_rules, input)
print(sum)

