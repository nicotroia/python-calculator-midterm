"""CSV-based calculation log, updated via the Observer pattern using pandas"""
from datetime import date
from pathlib import Path

import pandas as pd

from app.observer import Observer, CalculationEvent

_LOG_DIR = Path(__file__).parent.parent / "logs"

def _log_path() -> Path:
  """Return today's log file path, e.g. logs/2026-03-03.log"""
  return _LOG_DIR / f"{date.today()}.log"

class CalculatorLogger(Observer):
  """Appends each calculation to a date-stamped CSV log file via pandas

  The log directory is created automatically if it doesn't exist
  """
  # Column order for the CSV
  _COLUMNS = ["timestamp", "operation", "a", "b", "result"]

  def __init__(self):
    _LOG_DIR.mkdir(exist_ok=True)
    self._path = _log_path()
    # Load existing records for today if the file already exists
    if self._path.exists():
      self._df = pd.read_csv(self._path)
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
    self._df.to_csv(self._path, index=False)
