"""Tests for OperationFactory."""
import pytest
from app.operations import OperationFactory, Add, Divide

def test_create_returns_correct_type():
  assert isinstance(OperationFactory.create("add"), Add)
  assert isinstance(OperationFactory.create("divide"), Divide)

def test_create_case_insensitive():
  op = OperationFactory.create("ADD")
  assert op.execute(1, 2) == 3

def test_create_unknown_raises():
  with pytest.raises(ValueError, match="Unknown operation"):
    OperationFactory.create("square_root")

def test_execute_add():
  assert OperationFactory.execute("add", 3, 4) == 7

def test_execute_subtract():
  assert OperationFactory.execute("subtract", 10, 3) == 7

def test_execute_multiply():
  assert OperationFactory.execute("multiply", 6, 7) == 42

def test_execute_divide():
  assert OperationFactory.execute("divide", 10, 4) == 2.5

def test_execute_power():
  assert OperationFactory.execute("power", 2, 8) == 256

def test_execute_root():
  assert OperationFactory.execute("root", 27, 3) == pytest.approx(3.0)

def test_execute_modulus():
  assert OperationFactory.execute("modulus", 10, 3) == 1

def test_execute_integer_division():
  assert OperationFactory.execute("integer_division", 10, 3) == 3

def test_execute_percentage():
  assert OperationFactory.execute("percentage", 50, 200) == pytest.approx(25.0)

def test_execute_absolute_difference():
  assert OperationFactory.execute("absolute_difference", 3, 10) == 7

def test_execute_divide_by_zero_propagates():
  with pytest.raises(ValueError, match="Cannot divide by zero"):
    OperationFactory.execute("divide", 5, 0)
