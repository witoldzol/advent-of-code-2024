import copy
from collections import deque

f = open('testinput')
f = open('input10')
grid = []
for l in f:
    grid.append(list(l.rstrip()))

# print grid
for l in grid:
    print(l)

def score_traihead(start: tuple[int,int], grid: list[list[str]])->int:
    final_paths = set()
    start_x, start_y = start
    Q = deque()
    # use tuple of current-x, current-y, visited(set of tuples of x/y)
    Q.append((start_x, start_y, {(start_x, start_y)}, [(start_x, start_y)]))
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    while Q:
        x, y, visited, path = Q.popleft()
        for d in directions:
            dx, dy = d
            new_x = x + dx
            new_y = y + dy
            next_step = (new_x, new_y)
            # check if we are in bounds
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                # check if next step is 1 higher and not visited
                try:
                    a = int(grid[new_x][new_y])
                    b = int(grid[x][y])
                except:
                    continue
                # if visited is None:
                #     import pprint
                #     pprint.pprint(locals())
                if a - b == 1 and next_step not in visited:
                    # check if we reached the peak
                    if grid[new_x][new_y] == '9':
                        final_paths.add((new_x,new_y))
                    # otherwise keep walkin
                    else:
                        new_path = path[:]
                        new_path.append(next_step)
                        new_visited = copy.copy(visited)
                        new_visited.add(next_step)
                        Q.append((new_x, new_y, new_visited, new_path))
    return final_paths

score = 0
for x in range(len(grid)):
    for y in range(len(grid[0])):
        if grid[x][y] == '0':
            final_paths = score_traihead((int(x), int(y)), grid)
            # print(f"score for trailhead {x},{y} is {len(final_paths)}")
            score += len(final_paths)
            # for p in final_paths:
                # print(p)
print(score)
