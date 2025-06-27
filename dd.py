from functools import lru_cache


CACHE = {}

stones = open("testinput").read().strip().split(" ")
stones = open('input11').read().strip().split(' ')


# @lru_cache(maxsize=None)
def deep(n: int, iteration: int, max: int) -> int:
    x = (n,iteration, max)
    if x in CACHE:
        return CACHE[x]
    if iteration == max:
        a = len(transform(n))
        if x not in CACHE:
            CACHE[(n,iteration, max)] = a
        return a
    else:
        ans = transform(n)
        if len(ans) == 2:
            a, b = ans
            ax = deep(a, iteration + 1, max)
            if (a, iteration + 1, max) not in CACHE:
                CACHE[(a, iteration + 1, max)] = ax
            bx = deep(b, iteration + 1, max)
            if (b, iteration + 1, max) not in CACHE:
                CACHE[(b, iteration + 1, max)] = bx
            return ax + bx
        else:
            aa = deep(ans[0], iteration + 1, max)
            y = (ans[0], iteration + 1, max)
            if y not in CACHE:
                CACHE[y] = aa
            return aa


def transform(n: int) -> list[int]:
    if n == 0:
        return [1]
    # split into two halfs
    elif len(str(n)) % 2 == 0:
        num = str(n)
        mid = len(num) // 2
        left = num[:mid]
        if len(left) > 1:
            left = left.lstrip("0")
        if left == "":
            left = 0
        right = num[mid:]
        if len(right) > 1:
            right = right.lstrip("0")
        if right == "":
            right = 0
        return [int(left), int(right)]
    else:
        return [n * 2024]


iterations = 75
count = 0
for s in stones:
    x = (int(s), 0, iterations-1)
    count += deep(int(s), 0, iterations-1)
print(count)
