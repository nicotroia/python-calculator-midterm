"""Tests for input_validators"""
from decimal import Decimal
import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator, parse_expression, parse_word_command

# ── valid expressions

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

# ── invalid expressions

@pytest.mark.parametrize("expr", [
  "abc",
  "1 2",
  "+ 2",
  "1 +",
  "",
  "1 @ 2",
])
def test_parse_invalid(expr):
  with pytest.raises(ValidationError):
    parse_expression(expr)

def test_parse_invalid_float_a():
  # Regex matches but float() conversion fails for a
  with pytest.raises(ValidationError, match="Invalid number"):
    parse_expression("1.2.3 + 4")

def test_parse_invalid_float_b():
  # Regex matches but float() conversion fails for b
  with pytest.raises(ValidationError, match="Invalid number"):
    parse_expression("4 + 1.2.3")

def test_validate_number_exceeds_max():
  cfg = CalculatorConfig()
  cfg.max_input_value = 100
  with pytest.raises(ValidationError, match="exceeds maximum"):
    InputValidator.validate_number("101", cfg)

def test_parse_expression_exceeds_max():
  cfg = CalculatorConfig()
  cfg.max_input_value = 10
  with pytest.raises(ValidationError, match="exceeds maximum"):
    parse_expression("999 + 1", cfg)

# ── parse_word_command

@pytest.mark.parametrize("text,op", [
  ("add 1 2",          "add"),
  ("subtract 5 3",     "subtract"),
  ("multiply 3 4",     "multiply"),
  ("divide 10 2",      "divide"),
  ("power 2 8",        "power"),
  ("root 27 3",        "root"),
  ("modulus 10 3",     "modulus"),
  ("mod 10 3",         "modulus"),
  ("int_divide 10 3",  "integer_division"),
  ("percent 50 200",   "percentage"),
  ("abs_diff 3 10",    "absolute_difference"),
])
def test_parse_word_command_valid(text, op):
  a, name, b = parse_word_command(text)
  assert name == op

def test_parse_word_command_unknown_op():
  with pytest.raises(ValidationError, match="Unknown operation"):
    parse_word_command("square_root 9 0")

def test_parse_word_command_bad_format():
  with pytest.raises(ValidationError):
    parse_word_command("add 5")

def test_parse_word_command_invalid_number():
  with pytest.raises(ValidationError):
    parse_word_command("add abc 3")
