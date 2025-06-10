import sys
x = int(sys.argv[1])
y = int(sys.argv[2])
print(x, y)
f = open('testinput')
grid = []
for r in f:
    grid.append(list(r))
grid[x][y] = 'O'
for r in grid:
    print(''.join(r))
