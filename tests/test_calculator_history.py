"""Tests for CalculatorHistory observer"""
import textwrap
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

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


# --- load_from_csv ---

_VALID_CSV = textwrap.dedent("""\
  operation,operands,result,timestamp
  add,"1, 2",3,2026-03-07T10:00:00
  multiply,"3, 4",12,2026-03-07T10:01:00
""")

def test_load_from_csv_valid(tmp_path):
  csv_file = tmp_path / "history.csv"
  csv_file.write_text(_VALID_CSV)
  h = CalculatorHistory()
  events = h.load_from_csv(csv_file)
  assert len(events) == 2
  assert events[0].operation == "add"
  assert events[0].a == Decimal("1")
  assert events[0].b == Decimal("2")
  assert events[0].result == 3.0
  assert events[1].operation == "multiply"


def test_load_from_csv_file_not_found(tmp_path):
  h = CalculatorHistory()
  events = h.load_from_csv(tmp_path / "does_not_exist.csv")
  assert events == []


def test_load_from_csv_missing_columns(tmp_path):
  csv_file = tmp_path / "bad.csv"
  csv_file.write_text("op,nums\nadd,\"1,2\"\n")
  h = CalculatorHistory()
  events = h.load_from_csv(csv_file)
  assert events == []


def test_load_from_csv_malformed_row_skipped(tmp_path):
  csv_file = tmp_path / "partial.csv"
  csv_file.write_text(textwrap.dedent("""\
    operation,operands,result,timestamp
    add,"1, 2",3,2026-03-07T10:00:00
    subtract,INVALID,not_a_number,bad-ts
    multiply,"3, 4",12,2026-03-07T10:01:00
  """))
  h = CalculatorHistory()
  events = h.load_from_csv(csv_file)
  # Only the two valid rows should come back
  assert len(events) == 2
  assert events[0].operation == "add"
  assert events[1].operation == "multiply"


def test_load_from_csv_empty_file(tmp_path):
  csv_file = tmp_path / "empty.csv"
  csv_file.write_text("operation,operands,result,timestamp\n")
  h = CalculatorHistory()
  events = h.load_from_csv(csv_file)
  assert events == []


# --- save_to_csv ---

def test_save_to_csv_creates_file(tmp_path):
  config = SimpleNamespace(history_folder=str(tmp_path))
  h = CalculatorHistory()
  h.update(_ev("add", 1, 2, 3))
  h.save_to_csv(config)
  csv_files = list(tmp_path.glob("*.log"))
  assert len(csv_files) == 1

def test_save_to_csv_content(tmp_path):
  config = SimpleNamespace(history_folder=str(tmp_path))
  h = CalculatorHistory()
  h.update(_ev("multiply", 3, 4, 12))
  h.save_to_csv(config)
  content = next(tmp_path.glob("*.log")).read_text()
  assert "multiply" in content
  assert "3, 4" in content
  assert "12" in content

def test_save_to_csv_empty_history(tmp_path):
  config = SimpleNamespace(history_folder=str(tmp_path))
  h = CalculatorHistory()
  h.save_to_csv(config)
  csv_files = list(tmp_path.glob("*.log"))
  assert len(csv_files) == 1
  content = csv_files[0].read_text()
  # Only the header row, no data rows
  lines = [l for l in content.splitlines() if l.strip()]
  assert len(lines) == 1

def test_save_to_csv_creates_folder(tmp_path):
  nested = tmp_path / "a" / "b"
  config = SimpleNamespace(history_folder=str(nested))
  h = CalculatorHistory()
  h.update(_ev())
  h.save_to_csv(config)
  assert nested.exists()


# --- load_from_csv: unreadable file ---

def test_load_from_csv_unreadable(tmp_path):
  csv_file = tmp_path / "unreadable.csv"
  csv_file.write_text("anything")
  with patch("app.calculator_history.pd.read_csv", side_effect=OSError("disk error")):
    h = CalculatorHistory()
    events = h.load_from_csv(csv_file)
  assert events == []
