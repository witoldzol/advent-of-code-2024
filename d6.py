import copy
class Guard:
    def __init__(self, x: int, y: int) -> None:
        self.current = "up"
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
f = open('testinput')
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
            g = Guard(r,c)
        elif grid[r][c] == '#':
            x_axis.setdefault(r,[]).append(c)
            y_axis.setdefault(c,[]).append(r)
if g is None:
    raise Exception("Failed to init guard")

def is_on_right(i: int, obstacles:list[int]) -> int:
    sorted_obstacles = sorted(obstacles)
    for x in sorted_obstacles:
        if x > i:
            return x
    return -1

# walk until we go out of bounds
def traverse(g: Guard, matrix: list[list[str]], x_axis: dict[int,list[int]], y_axis: dict[int,list[int]]):
    grid = copy.deepcopy(matrix)
    while True:
        # check for alternatives before we move
        # alternatives depend on the direction we are facing
        # up -> right : y_axis
        # right -> down: x_axis
        # down -> left : y_axis
        # left -> up : x_axis
        if g.current == "up":
            if g.x in x_axis:
                next_blockade_on_right = is_on_right(g.y, x_axis[g.x])
                if next_blockade_on_right != -1:
                    print(f'we could go right from position {g.x} {g.y} to block {g.x}, {next_blockade_on_right}')
        x, y = g.move()
        if 0 <= g.x + x < len(grid) and 0 <= g.y + y < len(grid[0]):
            if grid[g.x + x][g.y + y] != '#':
                g.x = g.x + x
                g.y = g.y + y
                # print('moved to position', g.x, g.y, ' marking with X')
                grid[g.x][g.y] = 'X'
            else:
                # print('changing direction, from ', g.current, ' to ' )
                g.change_direction()
                print(g.current )
        else:
            break
    return grid
new_grid = traverse(g, grid, x_axis, y_axis)
# count all the steps
count = 0
for x in new_grid:
    for y in x:
        if y == 'X' or y == '^':
            count += 1
print(count)
