"""Tests for the Calculator class."""
import pytest
from app.calculator import Calculator


@pytest.fixture
def calc():
  return Calculator()


def test_add(calc):
  assert calc.calculate("add", 2, 3) == 5


def test_subtract(calc):
  assert calc.calculate("subtract", 5, 3) == 2


def test_multiply(calc):
  assert calc.calculate("multiply", 3, 4) == 12


def test_divide(calc):
  assert calc.calculate("divide", 10, 2) == 5
  assert calc.calculate("divide", 7, 2) == 3.5


def test_divide_by_zero(calc):
  with pytest.raises(ValueError, match="Cannot divide by zero"):
    calc.calculate("divide", 5, 0)


def test_unknown_operation(calc):
  with pytest.raises(ValueError, match="Unknown operation"):
    calc.calculate("square_root", 9, 0)
