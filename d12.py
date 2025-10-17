from pydantic import BaseModel
import pytest
from collections import deque
# from d12 import map_fields, Field


matrix = []
with open("./testinput12") as f:
    for line in f:
        fields = list(line.strip())
        matrix.append(fields)


class Field(BaseModel):
    area: int
    permiter: int


DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def parse_input_to_matrix(file_name: str) -> list[list[str]]:
    matrix = []
    with open(file_name) as f:
        for l in f:
            line = list(l.strip())
            matrix.append(line)
    return matrix


def explore_new_field(start_coords: tuple[int, int]) -> list[tuple[int, int]]:
    new_field = []
    queue = deque()
    queue.append(start_coords)


def map_fields_v2(matrix: list[list[str]]) -> dict[str, list[Field]] | None:
    if not matrix:
        return None
    visited = set()
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            # check if we were here already
            coords = (x, y)
            if coords in visited:
                continue
            visited.add(coords)
            # if we didn't visit this field before
            # that means it's a new field
            new_field = explore_new_field(coords)

    # while queue:
    #     current_cell = queue.popleft()
    #     for dx, dy in DIRECTIONS:
    #         print(dx, dy)
    #     # check left


def map_fields(matrix: list[list[str]]) -> dict[str, list[Field]]:
    area = {}
    for row in matrix:
        for cell in row:
            if cell in area:
                area[cell] += 1
            else:
                area[cell] = 1
    results = {}
    for k, v in area.items():
        if v == 1:
            p = 4
        elif v == 2:
            p = 6
        else:
            p = v * 2 + 2
        results[k] = [Field(area=v, permiter=p)]
    return results


########################################
########################################
########################################
########################################


@pytest.mark.parametrize(
    "input, expected",
    [
        ([["A"]], {"A": [Field(area=1, permiter=4)]}),
        ([["A", "A"]], {"A": [Field(area=2, permiter=6)]}),
        ([["A", "A", "A"]], {"A": [Field(area=3, permiter=8)]}),
    ],
)
def test_fields_in_1_row(input, expected):
    assert map_fields(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ([["A"], ["A"]], {"A": [Field(area=2, permiter=6)]}),
        ([["A"], ["A"], ["A"]], {"A": [Field(area=3, permiter=8)]}),
    ],
)
def test_field_in_1_column(input, expected):
    assert map_fields(input) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        # AA
        # AA
        ([["A", "A"], ["A", "A"]], {"A": [Field(area=4, permiter=8)]}),
    ],
)
def test_field_in_2_rows_columns(input, expected):
    assert map_fields(input) == expected


# def test_map_fields_v2():
#     matrix = [["A", "A"], ["A", "A"]]
#     expected = {"A": [Field(area=4, permiter=8)]}
#     assert map_fields_v2(matrix) == expected

map_fields_v2(parse_input_to_matrix("./testinput12"))
