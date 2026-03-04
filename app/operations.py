"""Arithmetic operation classes using the Abstract Base Class pattern."""
from abc import ABC, abstractmethod


class Operation(ABC):
    """Abstract base class for all calculator operations."""

    @abstractmethod
    def execute(self, a, b):
        """Perform the operation on two numbers and return the result."""


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
