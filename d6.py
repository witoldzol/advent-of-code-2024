import copy
from os import curdir
START_COORDS = None
OBSTACLES = set()
class Guard:
    def __init__(self, x: int, y: int, current = "up") -> None:
        self.current = current
        self.x = x
        self.y = y

    def move(self):
        if self.current == "up":
            return (-1,0)
        elif self.current == "right":
            return (0,1)
        elif self.current == "down":
            return (1,0)
        elif self.current == "left":
            return (0,-1)
        else:
            raise Exception('Wrong direction!')

    def change_direction(self):
        if self.current == "up":
            self.current = "right"
        elif self.current == "right":
            self.current = "down"
        elif self.current == "down":
            self.current = "left"
        else:
            self.current = "up"

    def __repr__(self) -> str:
        return f"Guard({self.x}, {self.y})"

f = open('input6')
# f = open('testinput')
grid = []
for l in f:
    grid.append(list(l.rstrip()))

# map obstacles
y_axis: dict[int, list[int]] = {}
x_axis: dict[int, list[int]]= {}
# init guard with start location
g = None
START_POSTITION_MARKER = "^"
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == START_POSTITION_MARKER:
            START_COORDS = (r,c)
            g = Guard(r,c)
        elif grid[r][c] == '#':
            x_axis.setdefault(r,[]).append(c)
            y_axis.setdefault(c,[]).append(r)
if g is None:
    raise Exception("Failed to init guard")

def next_obstacle(i: int, obstacles:list[int], reverse=False) -> int:
    sorted_obstacles = sorted(obstacles, reverse=reverse)
    # 1 2 3
    # 2
    # 3 2 1
    for x in sorted_obstacles:
        if reverse:
            if x < i:
                return x
        else:
            if x > i:
                return x
    return -1

# walk until we go out of bounds
def traverse_for_loop(g: Guard, grid: list[list[str]]):
    visited = set()
    visited.add((g.x, g.y, g.current))
    while True:
        x, y = g.move()
        if 0 <= g.x + x < len(grid) and 0 <= g.y + y < len(grid[0]):
            if grid[g.x + x][g.y + y] != '#':
                g.x = g.x + x
                g.y = g.y + y
                # check if we are in a loop
                if (g.x, g.y, g.current) in visited:
                    return True
                visited.add((g.x, g.y, g.current))
            else:
                g.change_direction()
                visited.add((g.x, g.y, g.current))
        else:
            break
    return False
# walk until we go out of bounds
def traverse(g: Guard, matrix: list[list[str]], x_axis: dict[int,list[int]], y_axis: dict[int,list[int]]):
    grid = copy.deepcopy(matrix)
    while True:
        x, y = g.move()
        if 0 <= g.x + x < len(grid) and 0 <= g.y + y < len(grid[0]):
            if grid[g.x + x][g.y + y] != '#':
                g.x = g.x + x
                g.y = g.y + y
                grid[g.x][g.y] = 'X'
            else:
                g.change_direction()
        else:
            break
    return grid

def is_infinite_loop(g: Guard, grid: list[list[str]], start_coords):
    visited = set()
    x , y = start_coords
    visited.add((x,y,"up"))
    while True:
        x, y = g.move()
        if 0 <= g.x + x < len(grid) and 0 <= g.y + y < len(grid[0]):
            if grid[g.x + x][g.y + y] != '#':
                if (g.x + x, g.y + y, g.current) in visited:
                    return 1
                g.x = g.x + x
                g.y = g.y + y
                visited.add((g.x, g.y, g.current))
            else:
                g.change_direction()
        else:
            return 0
new_grid = traverse(g, grid, x_axis, y_axis)

count = 0
for x in new_grid:
    for y in x:
        if y == 'X' or y == '^':
            count += 1
print(count)
loop_counter = 0
for x in range(len(new_grid)):
    for y in range(len(new_grid[0])):
        if new_grid[x][y] == 'X':
            new_grid[x][y] = '#'
            sx, sy = START_COORDS
            g = Guard(sx,sy)
            loop_counter += is_infinite_loop(g, new_grid, START_COORDS)
            new_grid[x][y] = 'X'
print(' loop counter ', loop_counter)

