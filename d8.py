f = open('input8')
# f = open('testinput')
locations = set()
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
            # print(a_type, ix,iy, '->', jx,jy)
            dx = ix - jx
            dy = iy - jy
            while 0<=ix+dx<len(grid) and 0<=iy+dy<len(grid[0]):
                grid[ix+dx][iy+dy] = '#'
                locations.add((ix+dx,iy+dy))
                ix = ix + dx
                iy = iy + dy

for l in grid:
    print(''.join(l))
a_count = 0
all_antena_locations = set()
for k,v in antenas.items():
    if len(v) > 2:
        all_antena_locations.update(set(v))
        a_count += len(v)
overlapping = all_antena_locations.intersection(locations)
print('answer:')
print(len(locations) + a_count - len(overlapping))
