from pydantic import BaseModel
import pytest
# from d12 import map_fields, Field


matrix = []
with open("./testinput12") as f:
    for line in f:
        fields = list(line.strip())
        matrix.append(fields)


class Field(BaseModel):
    area: int
    permiter: int


print(">" * 10)


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
