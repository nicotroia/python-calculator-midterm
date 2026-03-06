"""Tests for CalculatorHistory observer"""
from decimal import Decimal
from app.calculator_history import CalculatorHistory
from app.observer import CalculationEvent

def _ev(op="add", a=1, b=2, result=3):
  return CalculationEvent(op, Decimal(str(a)), Decimal(str(b)), result)

def test_starts_empty():
  h = CalculatorHistory()
  assert h.records == []

def test_update_adds_record():
  h = CalculatorHistory()
  h.update(_ev())
  assert len(h.records) == 1

def test_update_multiple():
  h = CalculatorHistory()
  h.update(_ev("add", 1, 2, 3))
  h.update(_ev("multiply", 3, 4, 12))
  assert len(h.records) == 2
  assert h.records[1].operation == "multiply"

def test_clear_empties_records():
  h = CalculatorHistory()
  h.update(_ev())
  h.clear()
  assert h.records == []

def test_display_empty():
  h = CalculatorHistory()
  assert "No history" in h.display()

def test_display_shows_operation():
  h = CalculatorHistory()
  h.update(_ev("add", 1, 2, 3))
  out = h.display()
  assert "add" in out
  assert "3" in out
