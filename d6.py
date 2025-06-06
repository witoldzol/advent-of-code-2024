from enum import Enum

class Guard:
    def __init__(self, x, y) -> None:
        self.current = "up"
        self.x = x
        self.y = y

    def get_direction(self):
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

f = open('./testinput')
grid = []
for l in f:
    grid.append(list(l.rstrip()))

# init guard with start location
guard = None
POSTITION_MARKER = "^"
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == POSTITION_MARKER:
            g = Guard(r,c)
if g is None:
    raise Exception("Failed to init guard")

print(g)
