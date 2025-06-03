"XMAS"
input = open('input4')
input = open('testinput')
matrix = []
for l in input:
    x = list(l.rstrip())
    matrix.append(x)

xmas_count  = 0
for x, row in enumerate(matrix):
    for y, c in enumerate(row):
        if c == 'X':
            # left to right
            if y + 3 < len(row):
                m = row[y+1]
                a = row[y+2]
                s = row[y+3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # right to left
            if y - 3 >= 0:
                m = row[y-1]
                a = row[y-2]
                s = row[y-3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # up
            if x - 3 >= 0:
                m = row[x-1]
                a = row[x-2]
                s = row[x-3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # down
            if x + 3 < len(matrix):
                m = row[x+1]
                a = row[x+2]
                s = row[x+3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # diagonal to up right
            if x - 3 >= 0 and y + 3 < len(row):
                m = matrix[x-1][y+1]
                a = matrix[x-2][y+2]
                s = matrix[x-3][y+3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # diagonal to up left
            if x - 3 >= 0 and y - 3 >= 0:
                m = matrix[x-1][y-1]
                a = matrix[x-2][y-2]
                s = matrix[x-3][y-3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # diagonal to down left
            if x + 3 < len(matrix) and y - 3 >= 0:
                m = matrix[x+1][y-1]
                a = matrix[x+2][y-2]
                s = matrix[x+3][y-3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
            # diagonal to down right
            if x + 3 < len(matrix) and y + 3 < len(row):
                m = matrix[x+1][y+1]
                a = matrix[x+2][y+2]
                s = matrix[x+3][y+3]
                if m == 'M' and a == 'A' and s == 'S':
                    xmas_count += 1
print(xmas_count)
