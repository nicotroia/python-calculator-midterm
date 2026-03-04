"""Tests for Operation subclasses"""
import pytest
from app.operations import (
    Operation,
    Add, Subtract, Multiply, Divide,
    Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference,
)

def test_operation_is_abstract():
  """Operation cannot be instantiated directly."""
  with pytest.raises(TypeError):
    Operation()

def test_add():
  op = Add()
  assert op.execute(2, 3) == 5
  assert op.execute(-1, 1) == 0
  assert op.execute(0, 0) == 0

def test_subtract():
  op = Subtract()
  assert op.execute(5, 3) == 2
  assert op.execute(0, 4) == -4
  assert op.execute(-2, -2) == 0

def test_multiply():
  op = Multiply()
  assert op.execute(3, 4) == 12
  assert op.execute(-2, 5) == -10
  assert op.execute(0, 100) == 0

def test_divide():
  op = Divide()
  assert op.execute(10, 2) == 5
  assert op.execute(7, 2) == 3.5
  assert op.execute(-6, 3) == -2

def test_divide_by_zero():
  op = Divide()
  with pytest.raises(ValueError, match="Cannot divide by zero"):
    op.execute(5, 0)

def test_power():
  op = Power()
  assert op.execute(2, 10) == 1024
  assert op.execute(5, 0) == 1
  assert op.execute(9, 0.5) == 3.0

def test_root():
  op = Root()
  assert op.execute(27, 3) == pytest.approx(3.0)
  assert op.execute(16, 4) == pytest.approx(2.0)

def test_root_zero_degree():
  op = Root()
  with pytest.raises(ValueError, match="Root degree cannot be zero"):
    op.execute(9, 0)

def test_modulus():
  op = Modulus()
  assert op.execute(10, 3) == 1
  assert op.execute(9, 3) == 0
  assert op.execute(7, 4) == 3

def test_modulus_by_zero():
  op = Modulus()
  with pytest.raises(ValueError, match="Cannot modulo by zero"):
    op.execute(5, 0)

def test_integer_division():
  op = IntegerDivision()
  assert op.execute(10, 3) == 3
  assert op.execute(9, 3) == 3
  assert op.execute(7, 2) == 3

def test_integer_division_by_zero():
  op = IntegerDivision()
  with pytest.raises(ValueError, match="Cannot divide by zero"):
    op.execute(5, 0)

def test_percentage():
  op = Percentage()
  assert op.execute(50, 200) == pytest.approx(25.0)
  assert op.execute(1, 4) == pytest.approx(25.0)
  assert op.execute(200, 200) == pytest.approx(100.0)

def test_percentage_by_zero():
  op = Percentage()
  with pytest.raises(ValueError, match="Cannot divide by zero"):
    op.execute(5, 0)

def test_absolute_difference():
  op = AbsoluteDifference()
  assert op.execute(10, 3) == 7
  assert op.execute(3, 10) == 7
  assert op.execute(-5, 5) == 10
  assert op.execute(4, 4) == 0
