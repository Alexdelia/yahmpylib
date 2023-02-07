from enum import Enum

import pytest

from src.attr.vals import vals
from src.testing import asrt


class _OBJEnum(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'


class _OBJ:
    d = 'D'
    e = 'E'
    f = 'F'


@pytest.fixture(scope="module")
def expected_vals_enum():
    return ['A', 'B', 'C']


@pytest.fixture(scope="module")
def expected_vals():
    return ['D', 'E', 'F']


def test_vals_enum(expected_vals_enum):
    asrt(vals(_OBJEnum), expected_vals_enum)


def test_vals(expected_vals):
    asrt(vals(_OBJ()), expected_vals)


def test_fail_vals_enum(expected_vals_enum):
    with pytest.raises(AssertionError):
        asrt(vals(_OBJEnum), expected_vals_enum + ['Z'])


def test_fail_vals(expected_vals):
    with pytest.raises(AssertionError):
        asrt(vals(_OBJ()), expected_vals + ['Z'])


def test_fail_vals_enum_type(expected_vals_enum):
    with pytest.raises(TypeError):
        asrt(vals(_OBJEnum()), expected_vals_enum)


def test_vals_type(expected_vals):
    asrt(vals(_OBJ), expected_vals)
