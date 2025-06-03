def is_safe(inputs: list[str], skip: int = -1) -> int:
    prev = None
    is_increasing = None
    for idx, x in enumerate(inputs):
        if skip == idx:
            continue
        if prev is None:
            prev = x
            continue
        if is_increasing is None:
            is_increasing = int(x) > int(prev)
        diff = abs(int(x) - int(prev))
        if diff < 1 or diff > 3:
            if skip == -1:
                first_try =  is_safe(inputs, skip=idx)
                second_try = 0
                if idx - 1 >= 0:
                    second_try =  is_safe(inputs, skip=idx - 1)
                third_try = 0
                if idx - 2 >= 0:
                    third_try =  is_safe(inputs, skip=idx - 2)
                return first_try or second_try or third_try
            return 0
        if is_increasing != (int(x) > int(prev)):
            if skip == -1:
                first_try =  is_safe(inputs, skip=idx)
                second_try = 0
                if idx - 1 >= 0:
                    second_try =  is_safe(inputs, skip=idx - 1)
                third_try = 0
                if idx - 2 >= 0:
                    third_try =  is_safe(inputs, skip=idx - 2)
                return first_try or second_try or third_try
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
