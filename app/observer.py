"""Observer pattern base classes for the calculator"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

@dataclass
class CalculationEvent:
  """Emitted after every successful calculation"""
  operation: str
  a: Decimal
  b: Decimal
  result: float
  timestamp: datetime = field(default_factory=datetime.now)

class Observer(ABC):
  """Abstract observer — implement update() to react to events"""

  @abstractmethod
  def update(self, event: CalculationEvent) -> None:
    """Receive a calculation event."""

class Observable:
  """Mixin that gives a class a list of observers and a notify method"""

  def __init__(self):
    self._observers: list[Observer] = []

  def add_observer(self, observer: Observer) -> None:
    self._observers.append(observer)

  def remove_observer(self, observer: Observer) -> None:
    self._observers.remove(observer)

  def notify_observers(self, event: CalculationEvent) -> None:
    for obs in self._observers:
      obs.update(event)
