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

count = 0
for s in stones:
    print(f'starting stone {s}')
    total = []
    total.append(int(s))
    for _ in range(iterations):
        temp = []
        for t in total:
            bob = transform(t)
            temp += bob
        total = temp
    count += len(total)
    print(f'finished stone {s}')

print(count)
