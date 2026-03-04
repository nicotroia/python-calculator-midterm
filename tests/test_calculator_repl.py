"""Tests for calculator_repl."""
import pytest
from app.calculator_repl import run, COMMANDS


# ── COMMANDS registry ────────────────────────────────────────────────────────

def test_commands_contains_help_and_exit():
  assert "help" in COMMANDS
  assert "exit" in COMMANDS


def test_commands_have_descriptions():
  for name, desc in COMMANDS.items():
    assert isinstance(desc, str) and desc, f"'{name}' has no description"


# ── run() integration via monkeypatched input ────────────────────────────────

def _run_with(inputs: list, monkeypatch, capsys):
  """Drive the REPL with a sequence of input strings, return printed output."""
  responses = iter(inputs)
  monkeypatch.setattr("builtins.input", lambda _: next(responses))
  run()
  return capsys.readouterr().out


def test_exit_command(monkeypatch, capsys):
  out = _run_with(["exit"], monkeypatch, capsys)
  assert "Goodbye" in out


def test_help_lists_commands(monkeypatch, capsys):
  out = _run_with(["help", "exit"], monkeypatch, capsys)
  for name in COMMANDS:
    assert name in out


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
  out = _run_with(["abc", "exit"], monkeypatch, capsys)
  assert "Error" in out


def test_divide_by_zero_shows_error(monkeypatch, capsys):
  out = _run_with(["5/0", "exit"], monkeypatch, capsys)
  assert "Error" in out


def test_empty_input_ignored(monkeypatch, capsys):
  out = _run_with(["", "exit"], monkeypatch, capsys)
  # Should not crash; just print the goodbye
  assert "Goodbye" in out


def test_keyboard_interrupt_graceful(monkeypatch, capsys):
  monkeypatch.setattr("builtins.input", lambda _: (_ for _ in ()).throw(KeyboardInterrupt))
  run()
  out = capsys.readouterr().out
  assert "Goodbye" in out
