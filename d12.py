from pydantic import BaseModel, ConfigDict
import pytest
import logging
from collections import deque
from typing import Tuple

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

matrix = []
# with open("./testinput12") as f:
# with open("./testinput12-2") as f:
# with open("./testinput12-3") as f:
with open("./input12") as f:
    for line in f:
        fields = list(line.strip())
        matrix.append(fields)


class Coordinates(BaseModel):
    model_config = ConfigDict(frozen=True)
    x: int
    y: int


class Field(BaseModel):
    area: int
    perimiter: int
    coordinates: set[Coordinates]


DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _is_empty(matrix: list[list[str]]) -> bool:
    if matrix is None or not matrix:
        return True
    return not any(row for row in matrix)


def _is_in_bounds(x: int, y: int, matrix: list[list[str]]) -> bool:
    return x >= 0 and x < len(matrix) and y >= 0 and y < len(matrix[0])


def explore_new_field(
    start: Coordinates, matrix: list[list[str]], visited: set[Coordinates]
) -> set[Coordinates]:
    if not _is_in_bounds(start.x, start.y, matrix):
        return set()
    field_type = matrix[start.x][start.y]
    new_field = set()
    new_field.add(start)
    visited.add(Coordinates(x=start.x, y=start.y))
    queue = deque()
    queue.append(start)
    while queue:
        c = queue.popleft()
        # check directions
        for dx, dy in DIRECTIONS:
            xx = c.x + dx
            yy = c.y + dy
            if not _is_in_bounds(xx, yy, matrix):
                continue
            if Coordinates(x=xx, y=yy) in visited:
                continue
            if matrix[xx][yy] == field_type:
                new_field.add(Coordinates(x=xx, y=yy))
                visited.add(Coordinates(x=xx, y=yy))
                queue.append(Coordinates(x=xx, y=yy))
    return new_field


def calculate_perimiter(field_coordinates: set[Coordinates]) -> int:
    count = 0
    # X == permiter
    # A = field
    #   X
    # X A X
    # X A A X
    #   X X
    for c in field_coordinates:
        for dx, dy in DIRECTIONS:
            xx = dx + c.x
            yy = dy + c.y
            # check every direction away from every part of a field,
            # if it's not a part of a field
            # that means it's a perimiter
            if Coordinates(x=xx, y=yy) not in field_coordinates:
                count += 1
    return count


def get_neighbour_coordinates_that_match_edge(
    edge_direction: tuple[int, int],
    matrix: list[list[str]],
    start_position: Coordinates,
) -> tuple[int, int] | None:
    """detectes if neighbor exists, doesn't check if neighbor is a part of the edge"""
    x, y = edge_direction
    assert x >= -1 or x <= 1
    assert y >= -1 or y <= 1
    # to turn 'right' depends on initial direction
    # initial direction (-1,0), so we move in X axis
    # turn right -> change original axis to 0
    # update the other axis with the same value
    # example:
    # start 0,0
    # direction -1,0
    # edge points here
    # _
    # ^
    # |
    # A A
    # 'right' of a 0,0 cell that has edge towards -1,0 is === 0,1, and 0,1 has an edge at -1,1 ( with direction of -1,0)
    # ----------
    # start 0,0
    # direction 1,0
    # _ _ _
    # _ A A
    # _ _ _
    # right is 0, -1 ( in this case empty )
    # ----------
    # start 0,0
    # direction 1,0
    # _ _ _
    # _ A A
    # _ _ _
    # right is 0, -1
    if x:
        xx = start_position.x
        yy = x * (-1) + start_position.y
    else:
        xx = y * (-1) + start_position.x
        yy = start_position.y
    field_type = matrix[start_position.x][start_position.y]
    if _is_in_bounds(xx, yy, matrix) and matrix[xx][yy] == field_type:
        logger.debug(
            f"NEIGHBOUR DETECTED for node ({start_position.x},{start_position.y}) -> ({xx},{yy})"
        )
        return (xx, yy)
    return None


XYCoords = Tuple[int, int]


def deduplicate_edges(
    edges: list[tuple[XYCoords, set[XYCoords]]],
) -> dict[tuple[XYCoords], list[set[XYCoords]]]:
    deduplicated_direction_to_edges = {}
    direction_to_edge: dict[XYCoords, list[set[XYCoords]]] = {}
    for edge in edges:
        direction = edge[0]
        set_of_coords = edge[1]
        if direction in direction_to_edge:
            direction_to_edge[direction].append(set_of_coords)
        else:
            direction_to_edge[direction] = [set_of_coords]
    # we need to sort by lenght first because, logically, a shorter set cannot be a superset of a longer one
    for direction, list_of_sets_of_coords in direction_to_edge.items():
        sorted_coords = sorted(
            list_of_sets_of_coords, key=lambda x: len(x), reverse=True
        )
        for sc in sorted_coords:
            if direction in deduplicated_direction_to_edges:
                if any(
                    sc.issubset(set_of_coords)
                    for set_of_coords in deduplicated_direction_to_edges[direction]
                ):
                    continue
                else:
                    deduplicated_direction_to_edges[direction].append(sc)
            else:
                deduplicated_direction_to_edges[direction] = [sc]
    return deduplicated_direction_to_edges


def get_edges(
    field_coordinates: set[Coordinates], matrix: list[list[str]]
) -> list[list[tuple[int, int], set[tuple[int, int]]]]:
    logger.debug(f"GETTING EDGES -> fields: {field_coordinates}")
    result = []
    for c in field_coordinates:
        # for dx, dy in [ (1, 0), (0, 1), ]:  # subset of direction, we only need to check x and y axis
        logger.debug(f"START new node: ({c.x, c.y})")
        for dx, dy in DIRECTIONS:
            edge = set()  # field can be an edge in any direction
            logger.debug(f"  DIRECTION : ({dx, dy})")
            xx = dx + c.x
            yy = dy + c.y
            # if this cell is an edge
            if not _is_in_bounds(xx, yy, matrix) or matrix[xx][yy] != matrix[c.x][c.y]:
                logger.debug(
                    f"      NODE: ({c.x, c.y}) is an EDGE in direction ({dx, dy})"
                )
                edge.add((c.x, c.y))
                # now extend the edge until we can
                start_position = c
                while True:
                    logger.debug(
                        f"start position: x: {start_position.x}, y: {start_position.y}"
                    )
                    neighbor_coords = get_neighbour_coordinates_that_match_edge(
                        edge_direction=(dx, dy),
                        matrix=matrix,
                        start_position=start_position,
                    )
                    if neighbor_coords is None:
                        # no neighbor in the direction of the edge
                        break
                    # check if neighbor is part of the edge
                    n_x, n_y = neighbor_coords
                    xx = n_x + dx
                    yy = n_y + dy
                    if (
                        not _is_in_bounds(xx, yy, matrix)
                        or matrix[xx][yy] != matrix[c.x][c.y]
                    ):
                        edge.add((n_x, n_y))
                        start_position = Coordinates(x=n_x, y=n_y)
                    else:
                        break
            if edge:
                result.append([(dx, dy), edge])
    return result


def map_fields(matrix: list[list[str]]) -> list[Field]:
    if _is_empty(matrix):
        return None
    visited = set()
    fields = []
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            # check if we were here already
            coords = Coordinates(x=x, y=y)
            if coords in visited:
                continue
            visited.add(coords)
            # if we didn't visit this field before
            # that means it's a new field
            field_coordinates = explore_new_field(coords, matrix, visited)
            area = len(field_coordinates)
            perimiter = calculate_perimiter(field_coordinates)
            fields.append(
                Field(area=area, perimiter=perimiter, coordinates=field_coordinates)
            )
    return fields


########################################
########################################
########################################
########################################


@pytest.mark.parametrize(
    "input, expected",
    [
        ([["A"]], [Field(area=1, perimiter=4, coordinates=set())]),
        ([["A", "A"]], [Field(area=2, perimiter=6, coordinates=set())]),
        ([["A", "A", "A"]], [Field(area=3, perimiter=8, coordinates=set())]),
    ],
)
def test_fields_in_1_row(input, expected):
    fields = map_fields(input)
    for f in fields:
        f.coordinates = set()
    assert fields == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ([["A"], ["A"]], [Field(area=2, perimiter=6, coordinates=set())]),
        ([["A"], ["A"], ["A"]], [Field(area=3, perimiter=8, coordinates=set())]),
    ],
)
def test_field_in_1_column(input, expected):
    fields = map_fields(input)
    for f in fields:
        f.coordinates = set()
    assert fields == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        # AA
        # AA
        (
            [["A", "A"], ["A", "A"]],
            [Field(area=4, perimiter=8, coordinates=set())],
        ),
    ],
)
def test_field_in_2_rows_columns(input, expected):
    fields = map_fields(input)
    for f in fields:
        f.coordinates = set()
    assert fields == expected


@pytest.mark.parametrize(
    "coordinates, matrix, expected",
    [
        # TODO check empty matrix in parent
        # ((0, 0), [[]], set()),
        # ((0, 0), [], set()),
        # ((0, 0), None, set()),
        ((0, 0), [["A"]], {Coordinates(x=0, y=0)}),
        ((0, 0), [["A", "A"]], {Coordinates(x=0, y=0), Coordinates(x=0, y=1)}),
        ((0, 0), [["A", "B"]], {Coordinates(x=0, y=0)}),
        (
            (0, 0),
            [["A", "A"], ["A", "A"]],
            {
                Coordinates(x=0, y=0),
                Coordinates(x=0, y=1),
                Coordinates(x=1, y=0),
                Coordinates(x=1, y=1),
            },
        ),
        (
            (0, 0),
            [["A", "B"], ["A", "A"]],
            {
                Coordinates(x=0, y=0),
                Coordinates(x=1, y=0),
                Coordinates(x=1, y=1),
            },
        ),
        (
            (0, 0),
            [["A", "B"], ["B", "A"]],
            {
                Coordinates(x=0, y=0),
            },
        ),
        (
            (1, 1),
            [["A", "B"], ["B", "A"]],
            {
                Coordinates(x=1, y=1),
            },
        ),
    ],
)
def test_explore_new_field(coordinates, matrix, expected):
    c = Coordinates(x=coordinates[0], y=coordinates[1])
    visited = set()
    assert expected == explore_new_field(c, matrix, visited)


@pytest.mark.parametrize(
    "matrix, expected",
    [
        (
            ["A"],
            [Field(area=1, perimiter=4, coordinates={Coordinates(x=0, y=0)})],
        ),
    ],
)
def test_map_fields(matrix, expected):
    assert map_fields(matrix) == expected


@pytest.mark.parametrize(
    "field, expected",
    [
        ({Coordinates(x=0, y=0)}, 4),
        ({Coordinates(x=0, y=0), Coordinates(x=0, y=1)}, 6),
        (
            {
                Coordinates(x=0, y=0),
                Coordinates(x=0, y=1),
                Coordinates(x=1, y=0),
                Coordinates(x=1, y=1),
            },
            8,
        ),
    ],
)
def test_calculate_perimiter(field, expected):
    assert expected == calculate_perimiter(field)


def test_get_neighbour_coordinates_that_match_edge():
    expected = None
    actual = get_neighbour_coordinates_that_match_edge(
        edge_direction=(0, 1), matrix=[["A", "A"]], start_position=Coordinates(x=0, y=0)
    )
    assert expected == actual
    expected = (0, 1)
    actual = get_neighbour_coordinates_that_match_edge(
        edge_direction=(-1, 0),
        matrix=[["A", "A"]],
        start_position=Coordinates(x=0, y=0),
    )
    assert expected == actual


def test_get_edges():
    expected = [
        [(-1, 0), {(0, 0)}],
        [(1, 0), {(0, 0)}],
        [(0, -1), {(0, 0)}],
        [(0, 1), {(0, 0)}],
    ]
    assert expected == get_edges(
        field_coordinates={Coordinates(x=0, y=0)}, matrix=[["A"]]
    )


def test_get_edges_2():
    expected = [
        [(-1, 0), {(0, 1), (0, 0)}],
        [(-1, 0), {(0, 1)}],
        [(1, 0), {(0, 1), (0, 0)}],
        [(1, 0), {(0, 0)}],
        [(0, -1), {(0, 0)}],
        [(0, 1), {(0, 1)}],
    ]
    res = get_edges(
        field_coordinates={Coordinates(x=0, y=0), Coordinates(x=0, y=1)},
        matrix=[["A", "A"]],
    )
    # print(res)
    assert sorted(expected) == sorted(res)


# print(matrix)
# input_name = "./input12"
fields = map_fields(matrix)
total = 0
for f in fields:
    c = f.coordinates
    area = f.area
    e = get_edges(c, matrix=matrix)
    deduped_edges = deduplicate_edges(e)
    edges = sum([len(v) for v in deduped_edges.values()])
    total += edges * area


print(">" * 100)
print(total)
print(">" * 100)

# price = 0
# for f in fields:
#     price += f.area * f.perimiter
# print(f"Total price: {price} for input {input_name}")
# test run
# print(turn_right_and_have_a_neighbour((0, 1), matrix, Coordinates(x=0, y=0)))
# count_edges({Coordinates(x=0, y=0)}, matrix)
# count_edges({Coordinates(x=0, y=0)}, [["A", "A"]])
# count_edges({Coordinates(x=0, y=0), Coordinates(x=0, y=1)}, matrix)
