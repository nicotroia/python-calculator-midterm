"""Input validation and expression parsing for the calculator REPL"""
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
@dataclass
class InputValidator:
  """Validates and sanitizes calculator inputs"""

  @staticmethod
  def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
    """Validate and convert input to Decimal

    Args:
      value: Input value to validate (str, int, float, or Decimal)

    Returns:
      Decimal: Validated and normalized number

    Raises:
      ValidationError: If the value is non-numeric or exceeds the maximum
    """
    try:
      if isinstance(value, str):
        value = value.strip()
      number = Decimal(str(value))
      if abs(number) > config.max_input_value:
        raise ValidationError(
          f"Value exceeds maximum allowed: {config.max_input_value}"
        )
      return number.normalize()
    except InvalidOperation as exc:
      raise ValidationError(f"Invalid number format: {value}") from exc

# Ordered so multi-char operators (**  //) are matched before single-char ones
# Keep this order: multi-char before single-char so regex alternation works
OPERATOR_SYMBOLS = {
  "**": "power",
  "//": "integer_division",
  "+":  "add",
  "-":  "subtract",
  "*":  "multiply",
  "/":  "divide",
  "%":  "modulus",
  "^": "power", # Alias for ** power
}

# Matches optional-negative number
_EXPR_RE = re.compile(
  r'^\s*(-?[\d.]+)\s*(\*\*|//|[+\-*/%^])\s*(-?[\d.]+)\s*$'
)

# Matches a chain expression when there is no leading operand
_CHAIN_RE = re.compile(
  r'^\s*(\*\*|//|[+\-*/%^])\s*(-?[\d.]+)\s*$'
)

# Maps REPL word commands → OperationFactory names
# Short aliases are included so users don't have to type the full name
WORD_COMMANDS = {
  "add":          "add",
  "subtract":     "subtract",
  "multiply":     "multiply",
  "divide":       "divide",
  "power":        "power",
  "root":         "root",
  "modulus":      "modulus",
  "mod":          "modulus",
  "int_divide":   "integer_division",
  "percent":      "percentage",
  "abs_diff":     "absolute_difference",
}

_DEFAULT_CONFIG = CalculatorConfig()

_WORD_CMD_RE = re.compile(
  r'^\s*(\w+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*$'
)

def parse_word_command(text: str, config: CalculatorConfig = None):
  """Parse a word-style command like 'add 5 3' or 'root 27 3'.

  Returns:
    (a: Decimal, operation_name: str, b: Decimal)

  Raises:
    ValidationError: If the format is wrong or numbers are invalid
  """
  if config is None:
    config = _DEFAULT_CONFIG

  match = _WORD_CMD_RE.match(text)
  if not match:
    raise ValidationError(
      f"Cannot parse '{text}' as a command "
      f"Expected: <operation> <number> <number>"
    )

  word, raw_a, raw_b = match.groups()
  op_name = WORD_COMMANDS.get(word.lower())
  if op_name is None:
    raise ValidationError(
      f"Unknown operation '{word}'. "
      f"Valid operations: {sorted(WORD_COMMANDS)}"
    )

  a = InputValidator.validate_number(raw_a, config)
  b = InputValidator.validate_number(raw_b, config)
  return a, op_name, b

def parse_chain_expression(text: str, last_result, config: CalculatorConfig = None):
  """Parse a chain expression like '* 2', using last_result as the first operand.

  Returns:
    (a: Decimal, operation_name: str, b: Decimal)

  Raises:
    ValidationError: If the format is wrong, numbers are invalid, or last_result is None.
  """
  if config is None:
    config = _DEFAULT_CONFIG

  if last_result is None:
    raise ValidationError("No previous result to chain from. Perform a calculation first.")

  match = _CHAIN_RE.match(text)
  if not match:
    raise ValidationError(
      f"Cannot parse '{text}' as a chain expression. "
      f"Expected: <operator> <number>  e.g. '* 2'"
    )

  symbol, raw_b = match.groups()
  a = InputValidator.validate_number(str(last_result), config)
  b = InputValidator.validate_number(raw_b, config)
  return a, OPERATOR_SYMBOLS[symbol], b

def is_chain_expression(text: str) -> bool:
  """Return True if the text looks like a chain expression (operator + number only)."""
  return bool(_CHAIN_RE.match(text))

def parse_expression(text: str, config: CalculatorConfig = None):
  """Parse an infix expression string like '1+2' or '8 * -3'.

  Returns:
    (a: Decimal, operation_name: str, b: Decimal)

  Raises:
    ValidationError: If the expression cannot be parsed or numbers are invalid.
  """
  if config is None:
    config = _DEFAULT_CONFIG

  match = _EXPR_RE.match(text)
  if not match:
    raise ValidationError(
      f"Cannot parse '{text}'. Expected format: <number> <operator> <number>\n"
      f"  Supported operators: {' '.join(OPERATOR_SYMBOLS)}"
    )

  raw_a, symbol, raw_b = match.groups()
  a = InputValidator.validate_number(raw_a, config)
  b = InputValidator.validate_number(raw_b, config)
  return a, OPERATOR_SYMBOLS[symbol], b
