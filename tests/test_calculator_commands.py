"""Tests for the Command pattern implementation."""
from unittest.mock import MagicMock, patch

from app.calculator_commands import (
  ClearCommand, CommandInvoker, ExitCommand, HelpCommand,
  HistoryCommand, RedoCommand, UndoCommand,
)

def make_history(undo_result=True, redo_result=True, display_text="history"):
  h = MagicMock()
  h.undo.return_value = undo_result
  h.redo.return_value = redo_result
  h.display.return_value = display_text
  return h

# --- HelpCommand ---

def test_help_command_calls_help_fn():
  fn = MagicMock()
  assert HelpCommand(fn).execute() is True
  fn.assert_called_once()

# --- HistoryCommand ---

def test_history_command_prints_display(capsys):
  h = make_history(display_text="some history")
  assert HistoryCommand(h).execute() is True
  assert "some history" in capsys.readouterr().out

# --- ClearCommand ---

def test_clear_command_clears_and_prints(capsys):
  h = make_history()
  assert ClearCommand(h).execute() is True
  h.clear.assert_called_once()
  assert "History cleared." in capsys.readouterr().out

# --- UndoCommand ---

def test_undo_command_prints_undone(capsys):
  assert UndoCommand(make_history(undo_result=True)).execute() is True
  assert "Undone." in capsys.readouterr().out

def test_undo_command_prints_nothing_to_undo(capsys):
  assert UndoCommand(make_history(undo_result=False)).execute() is True
  assert "Nothing to undo." in capsys.readouterr().out

# --- RedoCommand ---

def test_redo_command_prints_redone(capsys):
  assert RedoCommand(make_history(redo_result=True)).execute() is True
  assert "Redone." in capsys.readouterr().out

def test_redo_command_prints_nothing_to_redo(capsys):
  assert RedoCommand(make_history(redo_result=False)).execute() is True
  assert "Nothing to redo." in capsys.readouterr().out

# --- ExitCommand ---

def test_exit_command_calls_goodbye_and_returns_false():
  fn = MagicMock()
  assert ExitCommand(fn).execute() is False
  fn.assert_called_once()

# --- CommandInvoker ---

def test_invoker_dispatches_registered_command():
  cmd = MagicMock()
  cmd.execute.return_value = True
  invoker = CommandInvoker()
  invoker.register("test", cmd)
  assert invoker.run("test") is True
  cmd.execute.assert_called_once()

def test_invoker_returns_none_for_unknown_command():
  assert CommandInvoker().run("unknown") is None

def test_invoker_returns_false_for_exit():
  goodbye = MagicMock()
  invoker = CommandInvoker()
  invoker.register("exit", ExitCommand(goodbye))
  assert invoker.run("exit") is False
