def is_safe(inputs: list[str]) -> int:
    prev = None
    is_increasing = None
    for x in inputs:
        if prev is None:
            prev = x
            continue
        if is_increasing is None:
            is_increasing = int(x) > int(prev)
        diff = abs(int(x) - int(prev))
        if diff < 1 or diff > 3:
            return 0
        if is_increasing != (int(x) > int(prev)):
            return 0
        prev = x
    return 1

f = open('input2')

safe_reports_count = 0
for l in f:
    inputs = l.rstrip().split()
    safe_reports_count += is_safe(inputs)
print('count')
print(safe_reports_count)
