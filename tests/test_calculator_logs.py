"""Tests for CalculatorLogger observer."""
from datetime import date
from decimal import Decimal
from types import SimpleNamespace

import pandas as pd
import pytest

from app.calculator_logs import CalculatorLogger
from app.observer import CalculationEvent


def _ev(op="add", a=1, b=2, result=3):
  return CalculationEvent(op, Decimal(str(a)), Decimal(str(b)), result)


def _config(tmp_path, encoding="utf-8"):
  return SimpleNamespace(log_dir=str(tmp_path), default_encoding=encoding)


def _today_log(tmp_path):
  return tmp_path / f"{date.today()}.log"


@pytest.fixture
def logger(tmp_path):
  return CalculatorLogger(_config(tmp_path))


def test_logger_creates_log_file(logger, tmp_path):
  logger.update(_ev())
  assert _today_log(tmp_path).exists()

def test_logger_writes_csv_columns(logger, tmp_path):
  logger.update(_ev("add", 2, 3, 5))
  df = pd.read_csv(_today_log(tmp_path))
  assert list(df.columns) == ["timestamp", "operation", "a", "b", "result"]

def test_logger_records_operation(logger, tmp_path):
  logger.update(_ev("multiply", 3, 4, 12))
  df = pd.read_csv(_today_log(tmp_path))
  assert df.iloc[0]["operation"] == "multiply"
  assert float(df.iloc[0]["result"]) == 12.0

def test_logger_appends_multiple_rows(logger, tmp_path):
  logger.update(_ev("add", 1, 2, 3))
  logger.update(_ev("subtract", 5, 3, 2))
  df = pd.read_csv(_today_log(tmp_path))
  assert len(df) == 2

def test_log_dir_is_created(tmp_path):
  target = tmp_path / "new_logs"
  CalculatorLogger(_config(target))
  assert target.exists()

def test_logger_loads_existing_log(tmp_path):
  log = _today_log(tmp_path)
  log.write_text("timestamp,operation,a,b,result\n2026-01-01T00:00:00,add,1,2,3\n")
  logger = CalculatorLogger(_config(tmp_path))
  logger.update(_ev("multiply", 3, 4, 12))
  df = pd.read_csv(log)
  assert len(df) == 2

def test_logger_default_config(tmp_path, monkeypatch):
  monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path))
  logger = CalculatorLogger()
  logger.update(_ev())
  assert _today_log(tmp_path).exists()

def test_logger_encoding_used(tmp_path):
  logger = CalculatorLogger(_config(tmp_path, encoding="utf-8"))
  logger.update(_ev("add", 1, 2, 3))
  assert _today_log(tmp_path).exists()
