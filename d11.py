import cProfile
import pstats
from collections import deque
from functools import lru_cache


stones = open('testinput').read().strip().split(' ')
stones = open('input11').read().strip().split(' ')

@lru_cache(maxsize=None)
def transform(n: int) -> list[int]:
    if n == 0:
        return [1]
    # split into two halfs
    elif len(str(n)) % 2 == 0:
        #print('splitting into two halfs num ' , str(n))
        num = str(n)
        mid = len(num) // 2
        left = num[:mid]
        if len(left) > 1:
            left = left.lstrip('0')
        if left == '':
            left = 0
        #print('left ', left)
        right = num[mid:]
        if len(right) > 1:
            right = right.lstrip('0')
        if right == '':
            right = 0
        #print('right ', right)
        return [int(left), int(right)]
    else:
        # #print('multiply by 2024 ', n)
        return [n * 2024]


iterations = 37

@lru_cache(maxsize=None)
def transform_stone_series(ss: int, ii: int) -> int:
    total = []
    total.append(int(ss))
    for _ in range(ii):
        temp = []
        for t in total:
            temp += transform(t)
        total = temp
    return len(total)

profiler = cProfile.Profile()
profiler.enable()
count = 0
for s in stones:
    print(f'starting stone {s}')
    
    count += transform_stone_series(s, iterations)
    print(f'finished stone {s}')

profiler.disable()
profiler.dump_stats('stats')
stats = pstats.Stats('stats').print_stats()

print(count)
