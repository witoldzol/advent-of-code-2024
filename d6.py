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

    def is_obstacle_ahead(self, grid):
        x, y = self.move()
        if 0 <= self.x + x < len(grid) and 0 <= self.y + y < len(grid[0]):
            if grid[self.x + x][self.y + y] == "#":
                return True
        return False

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
def traverse(g: Guard, matrix: list[list[str]], x_axis: dict[int,list[int]], y_axis: dict[int,list[int]]):
    grid = copy.deepcopy(matrix)
    while True:
        # check for alternatives before we move
        # alternatives depend on the direction we are facing
        # up -> right : y_axis
        if not g.is_obstacle_ahead(grid):
            if g.current == "up":
                if g.x in x_axis:
                    next_blockade = next_obstacle(g.y, x_axis[g.x])
                    if next_blockade != -1:
                        print(f'we could go right from position {g.x} {g.y} to block {g.x}, {next_blockade}')
            # right -> down: x_axis
            if g.current == "right":
                # if we go right, that means we traverse y axis, and potential pivot is down, so we need to check obstacles in x axis
                if g.y in y_axis:
                    next_blockade = next_obstacle(g.x, y_axis[g.y])
                    if next_blockade != -1:
                        print(f'we could go down from position {g.x} {g.y} to block {next_blockade}, {g.y}')
        # down -> left : y_axis
            if g.current == "down":
                # if we go down, that means we traverse x axis, and potential pivot is left, so we need to check obstacles in y axis
                if g.x in x_axis:
                    # reverse because we go 'left', meaning we look at the values lower than current y in y axis
                    next_blockade = next_obstacle(g.y, x_axis[g.x], reverse=True)
                    if next_blockade != -1:
                        print(f'we could go left from position {g.x} {g.y} to block {g.x}, {next_blockade}')
        # left -> up : x_axis
            if g.current == "left":
                # if we go left, that means we traverse y axis, and potential pivot is up, so we need to check obstacles in x axis
                if g.y in y_axis:
                    # reverse because we go 'up', meaning we look at the values lower than current x in x axis
                    next_blockade = next_obstacle(g.x, y_axis[g.y], reverse=True)
                    if next_blockade != -1:
                        print(f'we could go up from position {g.x} {g.y} to block {next_blockade}, {g.y}')
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
