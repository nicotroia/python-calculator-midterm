"""In-memory calculation history, updated via the Observer pattern"""
import logging
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd

from app.observer import Observer, CalculationEvent

logger = logging.getLogger(__name__)

class CalculatorHistory(Observer):
  """Stores each calculation in a list

  Register with an Observable and every successful
  calculation will automatically appear in self.records
  """
  def __init__(self):
    self.records: list[CalculationEvent] = []

  def update(self, event: CalculationEvent) -> None:
    self.records.append(event)

  def clear(self) -> None:
    """Remove all stored records"""
    self.records.clear()

  def save_to_csv(self, config) -> None:
    """Convert history to a DataFrame and save to a date-stamped file in the configured folder"""
    folder = Path(config.history_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{date.today()}.log"
    rows = [
      {
        "operation": r.operation,
        "operands": f"{r.a}, {r.b}",
        "result": r.result,
        "timestamp": r.timestamp.isoformat(timespec="seconds"),
      }
      for r in self.records
    ]
    df = pd.DataFrame(rows, columns=["operation", "operands", "result", "timestamp"])
    df.to_csv(path, index=False)

  def load_from_csv(self, path) -> list[CalculationEvent]:
    """Read a CSV file and return a list of CalculationEvent instances.

    Skips malformed rows with a warning instead of raising.
    Returns an empty list if the file does not exist or has no valid rows.
    """
    path = Path(path)
    if not path.exists():
      logger.warning("History file not found: %s", path)
      return []

    try:
      df = pd.read_csv(path)
    except Exception as exc:
      logger.error("Could not read history file %s: %s", path, exc)
      return []

    required = {"operation", "operands", "result", "timestamp"}
    if not required.issubset(df.columns):
      logger.error(
        "Malformed CSV %s — expected columns %s, got %s",
        path, required, set(df.columns),
      )
      return []

    events: list[CalculationEvent] = []
    for idx, row in df.iterrows():
      try:
        a_str, b_str = str(row["operands"]).split(",", 1)
        a = Decimal(a_str.strip())
        b = Decimal(b_str.strip())
        result = float(row["result"])
        timestamp = datetime.fromisoformat(str(row["timestamp"]))
        events.append(CalculationEvent(str(row["operation"]), a, b, result, timestamp))
      except (ValueError, InvalidOperation) as exc:
        logger.warning("Skipping malformed row %s in %s: %s", idx, path, exc)

    return events

  def display(self) -> str:
    """Return a formatted string of all records (or a 'no history' message)"""
    if not self.records:
      return "No history yet."
    lines = []
    for i, r in enumerate(self.records, 1):
      lines.append(
        f"  {i:>3}. [{r.timestamp:%H:%M:%S}]  {r.a} {r.operation} {r.b} = {r.result}"
      )
    return "\n".join(lines)
