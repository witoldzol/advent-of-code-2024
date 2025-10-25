from pydantic import BaseModel, ConfigDict
import pytest
import logging
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

matrix = []
with open("./testinput12") as f:
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


def parse_input_to_matrix(file_name: str) -> list[list[str]]:
    matrix = []
    with open(file_name) as f:
        for l in f:
            line = list(l.strip())
            matrix.append(line)
    return matrix


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
    x, y = edge_direction
    assert x >= -1 or x <= 1
    assert y >= -1 or y <= 1
    # to turn 'right' depends on initial direction
    # initial direction (-1,0), so we move in X axis
    # turn right -> change original axis to 0
    # update the other axis with the same value
    if x:
        xx = 0
        yy = x
    else:
        yy = 0
        xx = y
    field_type = matrix[start_position.x][start_position.y]
    if _is_in_bounds(xx, yy, matrix) and matrix[xx][yy] == field_type:
        logger.info(
            f"NEIGHBOUR DETECTED for node ({start_position.x},{start_position.y}) -> ({xx},{yy})"
        )
        return (xx, yy)
    return None


def extend_edge(
    edge, start, edge_direction, neighbor_coords, matrix
) -> set[tuple[int, int]]:
    start_x, start_y = start
    e_dy, e_dy = edge_direction
    neighbor_x, neighbor_y = neighbor_coords
    return {(5, 5)}
    # check if we have a neighbor

    # if we do, check if neighbor is also and edge in the same direction
    # example
    # _ _
    # A A (first A is and edge if we look 'up' and it has a neighbor A, which is also and edge in the same direction)
    # example 2:
    # line1: _ A
    # line2: A A ( first A on line 2, has neighbor, but that neighbor is not edge if we look up)

    # xxx = dx + neighbor_x
    # yyy = dy + neighbor_y
    # if (
    #     not _is_in_bounds(xxx, yyy, matrix)
    #     or matrix[xxx][yyy] != matrix[start_x][start_y]
    # ):
    #     # if our neighbor is also and edge in the same direction, create an edge
    #     edge.add((neighbor_x, neighbor_y))
    #     # repeat this process until we hit an end
    #     print(f"found an edge {edge}")


def count_edges(field_coordinates: set[Coordinates], matrix: list[list[str]]) -> int:
    result = []
    for c in field_coordinates:
        # for dx, dy in [ (1, 0), (0, 1), ]:  # subset of direction, we only need to check x and y axis
        logger.info(f"START new node: ({c.x, c.y})")
        for dx, dy in DIRECTIONS:
            edge = set()  # field can be an edge in any direction
            logger.info(f"  DIRECTION : ({dx, dy})")
            xx = dx + c.x
            yy = dy + c.y
            # if this cell is an edge
            if not _is_in_bounds(xx, yy, matrix) or matrix[xx][yy] != matrix[c.x][c.y]:
                logger.info(
                    f"      NODE: ({c.x, c.y}) is an EDGE in direction ({dx, dy})"
                )
                edge.add((c.x, c.y))
                # check if we have a neighbor to the right or down
                # for ddx, ddy in [(0, 1), (1, 0)]:
                neighbor_coords = get_neighbour_coordinates_that_match_edge(
                    edge_direction=(dx, dy), matrix=matrix, start_position=c
                )
                if neighbor_coords is None:
                    # no neighbor in the direction of the edge
                    if edge:
                        result.append(edge)
                    continue

                extend_edge(
                    edge=edge,
                    start=(c.x, c.y),
                    edge_direction=(dx, dy),
                    neighbor_coords=neighbor_coords,
                    matrix=matrix,
                )

            # while Coordinates(x=xx, y=yy) not in field_coordinates:
            #     new_direction = turn_right_and_have_a_neighbour((xx, yy), matrix, c)
            #     if new_direction is None:
            #         break
            #     new_run.add((c, Coordinates(x=xx, y=yy)))
            #     xx, yy = new_direction
    return 5


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


# input_name = "./testinput12"
# fields = map_fields(parse_input_to_matrix(input_name))
# price = 0
# for f in fields:
#     price += f.area * f.perimiter
# print(f"Total price: {price} for input {input_name}")
#
# input_name = "./testinput12b"
# fields = map_fields(parse_input_to_matrix(input_name))
# price = 0
# for f in fields:
#     price += f.area * f.perimiter
# print(f"Total price: {price} for input {input_name}")
#
# input_name = "./input12"
# fields = map_fields(parse_input_to_matrix(input_name))
# price = 0
# for f in fields:
#     price += f.area * f.perimiter
# print(f"Total price: {price} for input {input_name}")
# test run
# print(turn_right_and_have_a_neighbour((0, 1), matrix, Coordinates(x=0, y=0)))
# count_edges({Coordinates(x=0, y=0)}, matrix)
count_edges({Coordinates(x=0, y=0)}, [["A", "A"]])
# count_edges({Coordinates(x=0, y=0), Coordinates(x=0, y=1)}, matrix)
