"""Custom exception hierarchy for the calculator application"""

class CalculatorError(Exception):
  """Base exception for all calculator-specific errors

  Catch this to handle any error raised by the calculator in one place
  """

class ValidationError(CalculatorError):
  """Raised when user input fails validation

  Triggered by non-numeric values, invalid expressions, or unsupported
  operator symbols in parse_expression()
  """

class OperationError(CalculatorError):
  """Raised when an arithmetic operation cannot be completed

  Examples: division by zero, zero-degree root, or requesting an operation
  name that does not exist in the factory
  """
