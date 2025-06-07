class Guard:
    def __init__(self, x, y) -> None:
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
grid = []
for l in f:
    grid.append(list(l.rstrip()))

# init guard with start location
g = None
START_POSTITION_MARKER = "^"
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == START_POSTITION_MARKER:
            g = Guard(r,c)
if g is None:
    raise Exception("Failed to init guard")

# walk until we go out of bounds
while True:
    x, y = g.move()
    if 0 <= g.x + x < len(grid) and 0 <= g.y + y < len(grid[0]):
        if grid[g.x + x][g.y + y] != '#':
            g.x = g.x + x
            g.y = g.y + y
            print('moved to position', g.x, g.y, ' marking with X')
            grid[g.x][g.y] = 'X'
        else:
            print('changing direction, from ', g.current, ' to ' )
            g.change_direction()
            print(g.current )
    else:
        break
# count all the steps
count = 0
for x in grid:
    for y in x:
        if y == 'X' or y == '^':
            count += 1
print(count)
