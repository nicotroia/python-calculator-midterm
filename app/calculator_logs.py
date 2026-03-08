"""CSV-based calculation log, updated via the Observer pattern using pandas"""
from datetime import date
from pathlib import Path

import pandas as pd

from app.calculator_config import CalculatorConfig
from app.observer import Observer, CalculationEvent


class CalculatorLogger(Observer):
  """Appends each calculation to a date-stamped CSV log file via pandas

  The log directory is created automatically if it doesn't exist
  """
  _COLUMNS = ["timestamp", "operation", "a", "b", "result"]

  def __init__(self, config: CalculatorConfig = None):
    if config is None:
      config = CalculatorConfig()
    log_dir = Path(config.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    self._path = log_dir / f"{date.today()}.log"
    self._encoding = config.default_encoding
    if self._path.exists():
      self._df = pd.read_csv(self._path, encoding=self._encoding)
    else:
      self._df = pd.DataFrame(columns=self._COLUMNS)

  def update(self, event: CalculationEvent) -> None:
    new_row = pd.DataFrame([{
      "timestamp": event.timestamp.isoformat(timespec="seconds"),
      "operation": event.operation,
      "a": str(event.a),
      "b": str(event.b),
      "result": event.result,
    }])
    self._df = pd.concat([self._df, new_row], ignore_index=True)
    self._df.to_csv(self._path, index=False, encoding=self._encoding)
