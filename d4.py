"XMAS"
input = open('input4')
input = open('testinput')
matrix = []
for l in input:
    x = list(l.rstrip())
    matrix.append(x)

xmas_count  = 0
for r in range(len(matrix)):
    for c in range(len(matrix[0])):
        if matrix[r][c] != "X": continue
        for rd in (-1,0,1):
            for cd in (-1,0,1):
                if rd == 0 and cd == 0: continue
                if 0 <= r + rd * 3 < len(matrix) and 0 <= c + cd * 3 < len(matrix[0]):
                    if matrix[r + rd][c + cd] == 'M' and matrix[r + rd * 2][c + cd * 2] == 'A' and matrix[r + rd * 3][c + cd * 3] == 'S':
                        xmas_count += 1
print(xmas_count)


