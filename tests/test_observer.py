"""Tests for observer base classes"""
from decimal import Decimal
from app.observer import Observer, Observable, CalculationEvent

class _RecordingObserver(Observer):
  def __init__(self):
    self.received = []

  def update(self, event):
    self.received.append(event)

def test_observable_notifies_observer():
  subject = Observable()
  obs = _RecordingObserver()
  subject.add_observer(obs)
  event = CalculationEvent("add", Decimal("1"), Decimal("2"), 3)
  subject.notify_observers(event)
  assert len(obs.received) == 1
  assert obs.received[0] is event

def test_observable_notifies_multiple_observers():
  subject = Observable()
  obs1, obs2 = _RecordingObserver(), _RecordingObserver()
  subject.add_observer(obs1)
  subject.add_observer(obs2)
  subject.notify_observers(CalculationEvent("add", Decimal("1"), Decimal("2"), 3))
  assert len(obs1.received) == 1
  assert len(obs2.received) == 1

def test_remove_observer():
  subject = Observable()
  obs = _RecordingObserver()
  subject.add_observer(obs)
  subject.remove_observer(obs)
  subject.notify_observers(CalculationEvent("add", Decimal("1"), Decimal("2"), 3))
  assert len(obs.received) == 0

def test_calculation_event_has_timestamp():
  event = CalculationEvent("add", Decimal("1"), Decimal("2"), 3)
  assert event.timestamp is not None
