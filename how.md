iterate every cell, use bfs to keep going until we find the whole field,
we check directions of every cell,
if in bounds and same, add to field
always add to visited(not always, only if it's a part of a new field)
add the next field cell the queue

EXPLORED = {}
START AT 0,0
EXPLORE
EXPLORED = {(0,0), (0,1), (1,0), (1,1)}
MAP_OF_FIELDS = {((0,0), (0,1), (1,0), (1,1)): "A"}
[
    ["A","A","B"],
    ["A","A","B"],
]
(0,0) (0,1) (0,2) 
(1,0) (1,1) (1,2)
BORDERS = SET() INPUT IS A SORTED TUPLE OF TUPLES ( X, Y)
AND THEN WE CAN JUST COUNT THE UNIQUE EDGES
OOP ?
CLASS BORDERS:
    DEF __INIT__(SELF)
        SELF.BORDERS = SET()
    DEF ADD(SELF, BORDERS: LIST[]):
        SELF.BORDERS.ADD(SORTED())
