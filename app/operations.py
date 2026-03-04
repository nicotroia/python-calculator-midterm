"""Arithmetic operation classes using the Abstract Base Class pattern"""
from abc import ABC, abstractmethod
class Operation(ABC):
  """Abstract base class for all calculator operations."""

  @abstractmethod
  def execute(self, a, b):
    """Perform the operation on two numbers and return the result"""
class Add(Operation):
  def execute(self, a, b):
    return a + b
class Subtract(Operation):
  def execute(self, a, b):
    return a - b
class Multiply(Operation):
  def execute(self, a, b):
    return a * b
class Divide(Operation):
  def execute(self, a, b):
    if b == 0:
      raise ValueError("Cannot divide by zero")
    return a / b
class Power(Operation):
  def execute(self, a, b):
    return a ** b
class Root(Operation):
  def execute(self, a, b):
    if b == 0:
      raise ValueError("Root degree cannot be zero")
    return a ** (1 / b)
class Modulus(Operation):
  def execute(self, a, b):
    if b == 0:
      raise ValueError("Cannot modulo by zero")
    return a % b
class IntegerDivision(Operation):
  def execute(self, a, b):
    if b == 0:
      raise ValueError("Cannot divide by zero")
    return a // b
class Percentage(Operation):
  """Computes (a / b) * 100."""
  def execute(self, a, b):
    if b == 0:
      raise ValueError("Cannot divide by zero")
    return (a / b) * 100
class AbsoluteDifference(Operation):
  def execute(self, a, b):
    return abs(a - b)
