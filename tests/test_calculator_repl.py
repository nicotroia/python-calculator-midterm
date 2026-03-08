"""Tests for calculator_repl."""
import pytest
from app.calculator_repl import run, COMMANDS

# ── COMMANDS registry

def test_commands_contains_required_keys():
  for key in ("help", "exit", "history", "clear"):
    assert key in COMMANDS

def test_commands_have_descriptions():
  for name, desc in COMMANDS.items():
    assert isinstance(desc, str) and desc, f"'{name}' has no description"

# ── helpers

def _run_with(inputs: list, monkeypatch, capsys):
  """Drive the REPL with a sequence of input strings, return printed output."""
  responses = iter(inputs)
  monkeypatch.setattr("builtins.input", lambda _: next(responses))
  run()
  return capsys.readouterr().out

# ── basic commands

def test_exit_command(monkeypatch, capsys):
  out = _run_with(["exit"], monkeypatch, capsys)
  assert "Goodbye" in out

def test_help_lists_commands(monkeypatch, capsys):
  out = _run_with(["help", "exit"], monkeypatch, capsys)
  for name in COMMANDS:
    assert name in out

def test_empty_input_ignored(monkeypatch, capsys):
  out = _run_with(["", "exit"], monkeypatch, capsys)
  assert "Goodbye" in out

def test_keyboard_interrupt_graceful(monkeypatch, capsys):
  monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))
  run()
  out = capsys.readouterr().out
  assert "Goodbye" in out

# ── infix expressions

def test_addition(monkeypatch, capsys):
  out = _run_with(["1+2", "exit"], monkeypatch, capsys)
  assert "3" in out

def test_subtraction(monkeypatch, capsys):
  out = _run_with(["10 - 3", "exit"], monkeypatch, capsys)
  assert "7" in out

def test_multiplication_with_spaces(monkeypatch, capsys):
  out = _run_with(["8 * 2", "exit"], monkeypatch, capsys)
  assert "16" in out

def test_division(monkeypatch, capsys):
  out = _run_with(["7/2", "exit"], monkeypatch, capsys)
  assert "3.5" in out

def test_power(monkeypatch, capsys):
  out = _run_with(["2**8", "exit"], monkeypatch, capsys)
  assert "256" in out

def test_integer_division(monkeypatch, capsys):
  out = _run_with(["10//3", "exit"], monkeypatch, capsys)
  assert "3" in out

def test_modulus(monkeypatch, capsys):
  out = _run_with(["10%3", "exit"], monkeypatch, capsys)
  assert "1" in out

def test_invalid_expression_shows_error(monkeypatch, capsys):
  out = _run_with(["???", "exit"], monkeypatch, capsys)
  assert "Error" in out

def test_divide_by_zero_shows_error(monkeypatch, capsys):
  out = _run_with(["5/0", "exit"], monkeypatch, capsys)
  assert "Error" in out

# ── word-style commands

def test_word_add(monkeypatch, capsys):
  out = _run_with(["add 5 3", "exit"], monkeypatch, capsys)
  assert "8" in out


def test_word_subtract(monkeypatch, capsys):
  out = _run_with(["subtract 10 4", "exit"], monkeypatch, capsys)
  assert "6" in out


def test_word_multiply(monkeypatch, capsys):
  out = _run_with(["multiply 6 7", "exit"], monkeypatch, capsys)
  assert "42" in out


def test_word_divide(monkeypatch, capsys):
  out = _run_with(["divide 10 4", "exit"], monkeypatch, capsys)
  assert "2.5" in out


def test_word_power(monkeypatch, capsys):
  out = _run_with(["power 2 8", "exit"], monkeypatch, capsys)
  assert "256" in out

def test_word_root(monkeypatch, capsys):
  out = _run_with(["root 9 2", "exit"], monkeypatch, capsys)
  assert "3" in out

def test_word_modulus(monkeypatch, capsys):
  out = _run_with(["modulus 10 3", "exit"], monkeypatch, capsys)
  assert "1" in out

def test_word_int_divide(monkeypatch, capsys):
  out = _run_with(["int_divide 10 3", "exit"], monkeypatch, capsys)
  assert "3" in out

def test_word_percent(monkeypatch, capsys):
  out = _run_with(["percent 50 200", "exit"], monkeypatch, capsys)
  assert "25" in out

def test_word_abs_diff(monkeypatch, capsys):
  out = _run_with(["abs_diff 3 10", "exit"], monkeypatch, capsys)
  assert "7" in out

# ── history and clear

def test_history_empty_at_start(monkeypatch, capsys):
  out = _run_with(["history", "exit"], monkeypatch, capsys)
  assert "No history" in out

def test_history_records_calculation(monkeypatch, capsys):
  out = _run_with(["add 2 3", "history", "exit"], monkeypatch, capsys)
  assert "add" in out

def test_clear_empties_history(monkeypatch, capsys):
  out = _run_with(["add 2 3", "clear", "history", "exit"], monkeypatch, capsys)
  assert "cleared" in out
  assert "No history" in out


# ── undo / redo

def test_undo_command_in_commands():
  assert "undo" in COMMANDS

def test_redo_command_in_commands():
  assert "redo" in COMMANDS

def test_undo_with_nothing_to_undo(monkeypatch, capsys):
  out = _run_with(["undo", "exit"], monkeypatch, capsys)
  assert "Nothing to undo" in out

def test_redo_with_nothing_to_redo(monkeypatch, capsys):
  out = _run_with(["redo", "exit"], monkeypatch, capsys)
  assert "Nothing to redo" in out

def test_undo_after_calculation(monkeypatch, capsys):
  out = _run_with(["add 1 2", "undo", "history", "exit"], monkeypatch, capsys)
  assert "Undone" in out
  assert "No history" in out

def test_redo_after_undo(monkeypatch, capsys):
  out = _run_with(["add 1 2", "undo", "redo", "history", "exit"], monkeypatch, capsys)
  assert "Redone" in out
  assert "add" in out
