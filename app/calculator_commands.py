"""Each REPL command is wrapped in its own object so we can register, swap, and call them without a huge if/else block"""
from abc import ABC, abstractmethod
from typing import Callable

from app.calculator_memento import HistoryManager

class Command(ABC):
  @abstractmethod
  def execute(self) -> bool:
    """Run the command. return True to keep the loop going, False to quit"""

class HelpCommand(Command):
  def __init__(self, help_fn: Callable[[], None]):
    self._help_fn = help_fn

  def execute(self) -> bool:
    self._help_fn()
    return True

class HistoryCommand(Command):
  def __init__(self, history: HistoryManager):
    self._history = history

  def execute(self) -> bool:
    print(self._history.display())
    return True

class ClearCommand(Command):
  def __init__(self, history: HistoryManager):
    self._history = history

  def execute(self) -> bool:
    self._history.clear()
    print("History cleared.")
    return True

class UndoCommand(Command):
  def __init__(self, history: HistoryManager):
    self._history = history

  def execute(self) -> bool:
    if self._history.undo():
      print("Undone.")
    else:
      print("Nothing to undo.")
    return True

class RedoCommand(Command):
  def __init__(self, history: HistoryManager):
    self._history = history

  def execute(self) -> bool:
    if self._history.redo():
      print("Redone.")
    else:
      print("Nothing to redo.")
    return True

class ExitCommand(Command):
  def __init__(self, goodbye_fn: Callable[[], None]):
    self._goodbye_fn = goodbye_fn

  def execute(self) -> bool:
    self._goodbye_fn()
    return False  # tells the REPL loop to stop

class CommandInvoker:
  """Keeps a registry of named commands"""

  def __init__(self):
    self._commands: dict[str, Command] = {}

  def register(self, name: str, command: Command) -> None:
    self._commands[name] = command

  def run(self, name: str) -> bool | None:
    """Look up and run a command by name — returns None if not found"""
    command = self._commands.get(name)
    if command is None:
      return None
    return command.execute()
