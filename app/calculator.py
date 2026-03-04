"""Calculator class"""
from app.operations import OperationFactory

class Calculator:
  """Stateless calculator that executes operations by name via OperationFactory"""

  def calculate(self, operation: str, a, b):
    """Execute a named operation on two numbers and return the result"""
    return OperationFactory.execute(operation, a, b)
