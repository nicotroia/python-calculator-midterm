"""Tests for input_validators."""
import pytest
from app.input_validators import parse_expression

# ── valid expressions ────────────────────

@pytest.mark.parametrize("expr,expected", [
  ("1+2",        (1.0, "add",              2.0)),
  ("8 * 2",      (8.0, "multiply",         2.0)),
  ("10 - 3",     (10.0, "subtract",        3.0)),
  ("9/3",        (9.0, "divide",           3.0)),
  ("2**8",       (2.0, "power",            8.0)),
  ("4^2",        (4.0, "power",            2.0)),
  ("10 // 3",    (10.0, "integer_division",3.0)),
  ("10 % 3",     (10.0, "modulus",         3.0)),
  ("-5 + 3",     (-5.0, "add",             3.0)),
  ("5 + -3",     (5.0, "add",             -3.0)),
  ("2.5 * 4",    (2.5, "multiply",         4.0)),
])
def test_parse_valid(expr, expected):
  assert parse_expression(expr) == expected

# ── invalid expressions ─────────────────────

@pytest.mark.parametrize("expr", [
  "abc",
  "1 2",
  "+ 2",
  "1 +",
  "",
  "1 @ 2",
])
def test_parse_invalid(expr):
  with pytest.raises(ValueError):
    parse_expression(expr)

def test_parse_invalid_float_a():
  # Regex matches but float() conversion fails for a
  with pytest.raises(ValueError, match="Invalid number"):
    parse_expression("1.2.3 + 4")

def test_parse_invalid_float_b():
  # Regex matches but float() conversion fails for b
  with pytest.raises(ValueError, match="Invalid number"):
    parse_expression("4 + 1.2.3")
