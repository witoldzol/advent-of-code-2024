# f = open('input8')
f = open('testinput')
grid = []
antenas = {}
for l in f:
    l = list(l.rstrip())
    grid.append(l)
for r in range(len(grid)):
    for c in range(len(grid[0])):
        x = grid[r][c]
        if x != '.':
            antenas.setdefault(x, []).append((r,c))
print(antenas)
for a_type,coords in antenas.items():
    for i in range(len(coords)):
        for j in range(len(coords)):
            # skip duplicated match
            if j == i:
                continue
            ix,iy = coords[i]
            jx,jy = coords[j]
            print(a_type, ix,iy, '->', jx,jy)



