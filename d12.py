from pydantic import BaseModel, ConfigDict
import pytest
from collections import deque


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


def calculate_perimiter_v2(field_coordinates: set[Coordinates]) -> int:
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


@pytest.mark.parametrize(
    "field, expected",
    [
        ({Coordinates(x=0, y=0)}, 4),
        ({Coordinates(x=0, y=0), Coordinates(x=0, y=1)}, 4),
        (
            {
                Coordinates(x=0, y=0),
                Coordinates(x=0, y=1),
                Coordinates(x=1, y=0),
                Coordinates(x=1, y=1),
            },
            4,
        ),
    ],
)
def test_calculate_perimiter_v2(field, expected):
    assert expected == calculate_perimiter_v2(field)


input_name = "./testinput12"
fields = map_fields(parse_input_to_matrix(input_name))
price = 0
for f in fields:
    price += f.area * f.perimiter
print(f"Total price: {price} for input {input_name}")

input_name = "./testinput12b"
fields = map_fields(parse_input_to_matrix(input_name))
price = 0
for f in fields:
    price += f.area * f.perimiter
print(f"Total price: {price} for input {input_name}")

input_name = "./input12"
fields = map_fields(parse_input_to_matrix(input_name))
price = 0
for f in fields:
    price += f.area * f.perimiter
print(f"Total price: {price} for input {input_name}")
