iterate every cell, use bfs to keep going until we find the whole field,
we check directions of every cell,
if in bounds and same, add to field
always add to visited(not always, only if it's a part of a new field)
add the next field cell the queue

EXPLORED = {}
START AT 0,0
EXPLORE
EXPLORED = {(0,0), (0,1), (1,0), (1,1)}
MAP_OF_FIELDS = [(0,0), (0,1), (1,0), (1,1)]
[
    ["A","A","B"],
    ["A","A","B"],
]
(0,0) (0,1) (0,2) 
(1,0) (1,1) (1,2)

calculate_edges()

