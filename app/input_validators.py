"""Input validation and expression parsing for the calculator REPL."""
import re

# Ordered so multi-char operators (**  //) are matched before single-char ones
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

# Matches optional-negative number  OP  optional-negative number
_EXPR_RE = re.compile(
  r'^\s*(-?[\d.]+)\s*(\*\*|//|[+\-*/%^])\s*(-?[\d.]+)\s*$'
)

def parse_expression(text: str):
  """Parse an expression string like '1+2' or '8 * -3'.

  Returns:
    (a: float, operation_name: str, b: float)

  Raises:
    ValueError if the expression cannot be parsed or numbers are invalid.
  """
  match = _EXPR_RE.match(text)
  if not match:
    raise ValueError(
      f"Cannot parse '{text}'. Expected format: <number> <operator> <number>\n"
      f"  Supported operators: {' '.join(OPERATOR_SYMBOLS)}"
    )

  raw_a, symbol, raw_b = match.groups()

  try:
    a = float(raw_a)
  except ValueError:
    raise ValueError(f"Invalid number: '{raw_a}'")

  try:
    b = float(raw_b)
  except ValueError:
    raise ValueError(f"Invalid number: '{raw_b}'")

  operation_name = OPERATOR_SYMBOLS[symbol]
  return a, operation_name, b
