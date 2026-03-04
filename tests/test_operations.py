"""Tests for Operation subclasses"""
import pytest
from app.operations import Add, Subtract, Multiply, Divide, Operation

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
