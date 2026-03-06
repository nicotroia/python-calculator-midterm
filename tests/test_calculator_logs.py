"""Tests for CalculatorLogger observer."""
from decimal import Decimal
from pathlib import Path

import pandas as pd
import pytest

from app.calculator_logs import CalculatorLogger, _LOG_DIR
from app.observer import CalculationEvent

def _ev(op="add", a=1, b=2, result=3):
  return CalculationEvent(op, Decimal(str(a)), Decimal(str(b)), result)

@pytest.fixture
def logger(tmp_path, monkeypatch):
  """Return a CalculatorLogger that writes to a temp directory."""
  monkeypatch.setattr("app.calculator_logs._LOG_DIR", tmp_path)
  # Patch _log_path so it also uses tmp_path
  import app.calculator_logs as mod
  monkeypatch.setattr(mod, "_log_path", lambda: tmp_path / "test.log")
  return CalculatorLogger()

def test_logger_creates_log_file(logger, tmp_path):
  logger.update(_ev())
  assert (tmp_path / "test.log").exists()

def test_logger_writes_csv_columns(logger, tmp_path):
  logger.update(_ev("add", 2, 3, 5))
  df = pd.read_csv(tmp_path / "test.log")
  assert list(df.columns) == ["timestamp", "operation", "a", "b", "result"]

def test_logger_records_operation(logger, tmp_path):
  logger.update(_ev("multiply", 3, 4, 12))
  df = pd.read_csv(tmp_path / "test.log")
  assert df.iloc[0]["operation"] == "multiply"
  assert float(df.iloc[0]["result"]) == 12.0

def test_logger_appends_multiple_rows(logger, tmp_path):
  logger.update(_ev("add", 1, 2, 3))
  logger.update(_ev("subtract", 5, 3, 2))
  df = pd.read_csv(tmp_path / "test.log")
  assert len(df) == 2

def test_log_dir_is_created(tmp_path, monkeypatch):
  target = tmp_path / "new_logs"
  import app.calculator_logs as mod
  monkeypatch.setattr(mod, "_LOG_DIR", target)
  monkeypatch.setattr(mod, "_log_path", lambda: target / "test.log")
  CalculatorLogger()
  assert target.exists()
