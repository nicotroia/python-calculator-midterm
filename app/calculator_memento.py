"""Calculator undo/redo functionality"""
from dataclasses import dataclass

from app.observer import CalculationEvent, Observer

@dataclass(frozen=True)
class Memento:
  """Immutable snapshot of the calculation history stack"""
  state: tuple[CalculationEvent, ...]

class HistoryManager(Observer):
  """Manages undo/redo for calculation history using the Memento pattern.

  Implements Observer so it can be registered directly with an Observable
  and receive CalculationEvents automatically.

  Usage:
    manager = HistoryManager()
    manager.push(event)   # record a new calculation
    manager.undo()        # revert last calculation
    manager.redo()        # re-apply last undone calculation
    manager.history       # current list of CalculationEvents
  """

  def __init__(self) -> None:
    self._history: list[CalculationEvent] = []
    self._undo_stack: list[Memento] = []
    self._redo_stack: list[Memento] = []

  # --- internal ---

  def _snapshot(self) -> Memento:
    return Memento(tuple(self._history))

  # --- public methods ---

  def update(self, event: CalculationEvent) -> None:
    """Observer hook — called automatically by Observable after each calculation"""
    self.push(event)

  def push(self, event: CalculationEvent) -> None:
    """Record a new calculation. Clears the redo stack"""
    self._undo_stack.append(self._snapshot())
    self._redo_stack.clear()
    self._history.append(event)

  def undo(self) -> bool:
    """Revert the last calculation. Returns True if undo was possible"""
    if not self._undo_stack:
      return False
    self._redo_stack.append(self._snapshot())
    self._history = list(self._undo_stack.pop().state)
    return True

  def redo(self) -> bool:
    """Re-apply the last undone calculation. Returns True if redo was possible"""
    if not self._redo_stack:
      return False
    self._undo_stack.append(self._snapshot())
    self._history = list(self._redo_stack.pop().state)
    return True

  def can_undo(self) -> bool:
    """Return True if there is at least one operation to undo"""
    return bool(self._undo_stack)

  def can_redo(self) -> bool:
    """Return True if there is at least one operation to redo"""
    return bool(self._redo_stack)

  def clear(self) -> None:
    """Remove all records and reset both stacks"""
    self._history.clear()
    self._undo_stack.clear()
    self._redo_stack.clear()

  def display(self) -> str:
    """Return a formatted string of all records (or a 'no history' message)"""
    if not self._history:
      return "No history yet."
    lines = []
    for i, r in enumerate(self._history, 1):
      lines.append(
        f"  {i:>3}. [{r.timestamp:%H:%M:%S}]  {r.a} {r.operation} {r.b} = {r.result}"
      )
    return "\n".join(lines)

  @property
  def history(self) -> list[CalculationEvent]:
    """Current calculation history (copy)"""
    return list(self._history)
