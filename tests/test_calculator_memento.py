"""Tests for HistoryManager (Memento pattern) — 100% coverage"""
from decimal import Decimal

import pytest

from app.calculator_memento import HistoryManager, Memento
from app.observer import CalculationEvent

def _ev(op="add", a=1, b=2, result=3) -> CalculationEvent:
  return CalculationEvent(op, Decimal(str(a)), Decimal(str(b)), result)

def test_memento_is_immutable():
  ev = _ev()
  m = Memento(state=(ev,))
  with pytest.raises((AttributeError, TypeError)):
    m.state = ()

def test_memento_stores_state():
  ev = _ev()
  m = Memento(state=(ev,))
  assert len(m.state) == 1
  assert m.state[0] is ev

# --- initial state ---

def test_initial_history_empty():
  ct = HistoryManager()
  assert ct.history == []

def test_initial_cannot_undo():
  ct = HistoryManager()
  assert not ct.can_undo()

def test_initial_cannot_redo():
  ct = HistoryManager()
  assert not ct.can_redo()

# --- push ---

def test_push_adds_to_history():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  assert len(ct.history) == 1
  assert ct.history[0].operation == "add"

def test_push_enables_undo():
  ct = HistoryManager()
  ct.push(_ev())
  assert ct.can_undo()

def test_push_clears_redo_stack():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.undo()
  assert ct.can_redo()       # redo available after undo
  ct.push(_ev("multiply", 3, 4, 12))
  assert not ct.can_redo()   # push must clear redo

def test_push_multiple():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.push(_ev("multiply", 3, 4, 12))
  assert len(ct.history) == 2

# --- history is a copy ---

def test_history_returns_copy():
  ct = HistoryManager()
  ct.push(_ev())
  h = ct.history
  h.clear()
  assert len(ct.history) == 1  # internal state must be unaffected

# --- undo ---

def test_undo_returns_false_when_empty():
  ct = HistoryManager()
  assert ct.undo() is False

def test_undo_returns_true_when_possible():
  ct = HistoryManager()
  ct.push(_ev())
  assert ct.undo() is True

def test_undo_removes_last_event():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.push(_ev("multiply", 3, 4, 12))
  ct.undo()
  assert len(ct.history) == 1
  assert ct.history[0].operation == "add"

def test_undo_to_empty():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  assert ct.history == []

def test_undo_enables_redo():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  assert ct.can_redo()

def test_undo_multiple_steps():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.push(_ev("subtract", 5, 3, 2))
  ct.push(_ev("multiply", 2, 4, 8))
  ct.undo()
  ct.undo()
  assert len(ct.history) == 1
  assert ct.history[0].operation == "add"

# --- redo ---

def test_redo_returns_false_when_empty():
  ct = HistoryManager()
  assert ct.redo() is False

def test_redo_returns_true_when_possible():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  assert ct.redo() is True

def test_redo_restores_event():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.undo()
  ct.redo()
  assert len(ct.history) == 1
  assert ct.history[0].operation == "add"

def test_redo_enables_undo():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  ct.redo()
  assert ct.can_undo()

def test_redo_multiple_steps():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.push(_ev("multiply", 3, 4, 12))
  ct.undo()
  ct.undo()
  ct.redo()
  ct.redo()
  assert len(ct.history) == 2
  assert ct.history[1].operation == "multiply"

# --- can_undo / can_redo ---

def test_can_undo_false_after_exhausted():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  assert not ct.can_undo()

def test_can_redo_false_after_exhausted():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  ct.redo()
  assert not ct.can_redo()

# --- update (Observer hook) ---

def test_update_calls_push():
  ct = HistoryManager()
  ev = _ev("add", 1, 2, 3)
  ct.update(ev)
  assert len(ct.history) == 1
  assert ct.history[0] is ev

def test_update_enables_undo():
  ct = HistoryManager()
  ct.update(_ev())
  assert ct.can_undo()

# --- clear ---

def test_clear_empties_history():
  ct = HistoryManager()
  ct.push(_ev())
  ct.clear()
  assert ct.history == []

def test_clear_resets_undo_stack():
  ct = HistoryManager()
  ct.push(_ev())
  ct.clear()
  assert not ct.can_undo()

def test_clear_resets_redo_stack():
  ct = HistoryManager()
  ct.push(_ev())
  ct.undo()
  ct.clear()
  assert not ct.can_redo()

# --- display ---

def test_display_empty():
  ct = HistoryManager()
  assert "No history" in ct.display()

def test_display_shows_operation():
  ct = HistoryManager()
  ct.push(_ev("multiply", 3, 4, 12))
  out = ct.display()
  assert "multiply" in out
  assert "12" in out

def test_display_numbers_entries():
  ct = HistoryManager()
  ct.push(_ev("add", 1, 2, 3))
  ct.push(_ev("subtract", 5, 3, 2))
  out = ct.display()
  assert "1." in out
  assert "2." in out
