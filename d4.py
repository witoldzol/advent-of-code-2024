# find "XMAS"
# M * S
# * A *
# M * S
input = open('input4')
matrix = []
for l in input:
    x = list(l.rstrip())
    matrix.append(x)

xmas_count  = 0
for r in range(len(matrix)):
    for c in range(len(matrix[0])):
        if matrix[r][c] != "A": continue
            # check boundaries
        if not(r + 1 < len(matrix) and c + 1 < len(matrix[0]) and r - 1 >= 0 and c - 1 >= 0): continue
        if (matrix[r-1][c-1] == 'M' and matrix[r-1][c+1] == 'M' and matrix[r+1][c-1] == 'S' and matrix[r+1][c+1] == 'S') or \
            (matrix[r-1][c-1] == 'S' and matrix[r-1][c+1] == 'S' and matrix[r+1][c-1] == 'M' and matrix[r+1][c+1] == 'M') or \
            (matrix[r-1][c-1] == 'M' and matrix[r-1][c+1] == 'S' and matrix[r+1][c-1] == 'M' and matrix[r+1][c+1] == 'S') or \
            (matrix[r-1][c-1] == 'S' and matrix[r-1][c+1] == 'M' and matrix[r+1][c-1] == 'S' and matrix[r+1][c+1] == 'M'):
            xmas_count += 1
print(xmas_count)
