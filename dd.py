CACHE = {}

stones = open("testinput").read().strip().split(" ")
stones = open('input11').read().strip().split(' ')


def deep(n: int, iteration: int, max: int) -> int:
    if iteration == max:
        return len(transform(n))
    else:
        ans = transform(n)
        if len(ans) == 2:
            a, b = ans
            return deep(a, iteration + 1, max) + deep(b, iteration + 1, max)
        else:
            return deep(ans[0], iteration + 1, max)


def transform(n: int) -> list[int]:
    # print('transfrming ', n)
    if n == 0:
        return [1]
    # split into two halfs
    elif len(str(n)) % 2 == 0:
        # print('splitting into two halfs num ' , str(n))
        num = str(n)
        mid = len(num) // 2
        left = num[:mid]
        if len(left) > 1:
            left = left.lstrip("0")
        if left == "":
            left = 0
        # print('left ', left)
        right = num[mid:]
        if len(right) > 1:
            right = right.lstrip("0")
        if right == "":
            right = 0
        # print('right ', right)
        return [int(left), int(right)]
    else:
        # #print('multiply by 2024 ', n)
        return [n * 2024]


iterations = 75
count = 0
for s in stones:
    if s in CACHE:
        ans = CACHE[s]
    else:
        ans = deep(int(s), 0, iterations-1)
        CACHE[s] = ans
    count += ans
print(count)
