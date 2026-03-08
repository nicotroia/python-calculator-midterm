"""Tests for CalculatorConfig — 100% coverage"""
import os
from decimal import Decimal

import pytest

from app.calculator_config import CalculatorConfig, _bool_env

# ── _bool_env helper

@pytest.mark.parametrize("val", ["true", "True", "TRUE", "1", "yes", "YES"])
def test_bool_env_truthy(val, monkeypatch):
  monkeypatch.setenv("TEST_FLAG", val)
  assert _bool_env("TEST_FLAG", False) is True

@pytest.mark.parametrize("val", ["false", "0", "no", "off", "anything"])
def test_bool_env_falsy(val, monkeypatch):
  monkeypatch.setenv("TEST_FLAG", val)
  assert _bool_env("TEST_FLAG", True) is False

def test_bool_env_missing_returns_default_true(monkeypatch):
  monkeypatch.delenv("TEST_FLAG", raising=False)
  assert _bool_env("TEST_FLAG", True) is True

def test_bool_env_missing_returns_default_false(monkeypatch):
  monkeypatch.delenv("TEST_FLAG", raising=False)
  assert _bool_env("TEST_FLAG", False) is False

# ── defaults (no env vars set)

def test_default_log_dir(monkeypatch):
  monkeypatch.delenv("CALCULATOR_LOG_DIR", raising=False)
  assert CalculatorConfig().log_dir == "logs"

def test_default_history_dir(monkeypatch):
  monkeypatch.delenv("CALCULATOR_HISTORY_DIR", raising=False)
  assert CalculatorConfig().history_dir == "logs"

def test_default_max_history_size(monkeypatch):
  monkeypatch.delenv("CALCULATOR_MAX_HISTORY_SIZE", raising=False)
  assert CalculatorConfig().max_history_size == 0

def test_default_auto_save(monkeypatch):
  monkeypatch.delenv("CALCULATOR_AUTO_SAVE", raising=False)
  assert CalculatorConfig().auto_save is True

def test_default_precision(monkeypatch):
  monkeypatch.delenv("CALCULATOR_PRECISION", raising=False)
  assert CalculatorConfig().precision == 10

def test_default_max_input_value(monkeypatch):
  monkeypatch.delenv("CALCULATOR_MAX_INPUT_VALUE", raising=False)
  monkeypatch.delenv("MAX_INPUT_VALUE", raising=False)
  assert CalculatorConfig().max_input_value == Decimal("1e10")

def test_default_encoding(monkeypatch):
  monkeypatch.delenv("CALCULATOR_DEFAULT_ENCODING", raising=False)
  assert CalculatorConfig().default_encoding == "utf-8"

# ── env var overrides

def test_log_dir_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_LOG_DIR", "/tmp/calc_logs")
  assert CalculatorConfig().log_dir == "/tmp/calc_logs"

def test_history_dir_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "/tmp/calc_history")
  assert CalculatorConfig().history_dir == "/tmp/calc_history"

def test_max_history_size_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
  assert CalculatorConfig().max_history_size == 50

def test_auto_save_false_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
  assert CalculatorConfig().auto_save is False

def test_auto_save_true_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "true")
  assert CalculatorConfig().auto_save is True

def test_precision_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_PRECISION", "4")
  assert CalculatorConfig().precision == 4

def test_max_input_value_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "9999")
  monkeypatch.delenv("MAX_INPUT_VALUE", raising=False)
  assert CalculatorConfig().max_input_value == Decimal("9999")

def test_max_input_value_legacy_fallback(monkeypatch):
  """CALCULATOR_MAX_INPUT_VALUE absent → falls back to old MAX_INPUT_VALUE."""
  monkeypatch.delenv("CALCULATOR_MAX_INPUT_VALUE", raising=False)
  monkeypatch.setenv("MAX_INPUT_VALUE", "5000")
  assert CalculatorConfig().max_input_value == Decimal("5000")

def test_default_encoding_from_env(monkeypatch):
  monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "latin-1")
  assert CalculatorConfig().default_encoding == "latin-1"

# ── mutability (dataclass fields are settable)

def test_config_fields_are_overridable():
  config = CalculatorConfig()
  config.precision = 2
  assert config.precision == 2
