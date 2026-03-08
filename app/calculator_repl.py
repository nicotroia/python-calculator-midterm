"""Interactive REPL for the calculator."""
import readline  # enables up/down arrow history in input()
from app.calculator_config import CalculatorConfig
from app.calculator_logs import CalculatorLogger
from app.calculator_memento import HistoryManager
from app.exceptions import CalculatorError, ValidationError
from app.input_validators import (
  parse_expression, parse_word_command, parse_chain_expression, is_chain_expression,
  OPERATOR_SYMBOLS, WORD_COMMANDS,
)
from app.observer import CalculationEvent, Observable
from app.operations import OperationFactory

# Each entry to be shown in help
COMMANDS = {
  "help":    "Show this help message",
  "history": "Display calculation history",
  "clear":   "Clear calculation history",
  "undo":    "Undo the last calculation",
  "redo":    "Re-apply the last undone calculation",
  "exit":    "Quit the calculator",
}

_OP_HELP = " | ".join(
  f"'{sym}' ({name})" for sym, name in OPERATOR_SYMBOLS.items()
)
_WORD_HELP = ", ".join(sorted(WORD_COMMANDS))

def _print_help():
  print("\n== Calculator Help ==")
  print("Infix:  <number> <operator> <number>")
  print(f"  Operators: {_OP_HELP}")
  print("Word:   <operation> <number> <number>")
  print(f"  Operations: {_WORD_HELP}")
  print("\nCommands:")
  for name, description in COMMANDS.items():
    print(f"  {name:<16} {description}")
  print()

class ReplLoop(Observable):
  """Runs the REPL loop and notifies observers of each calculation"""

  def __init__(self, config: CalculatorConfig):
    super().__init__()
    self._config = config
    self._last_result = None

  def _evaluate(self, raw: str):
    """Try word-command first, fall back to infix expression"""
    try:
      return parse_word_command(raw, self._config)
    except ValidationError:
      pass
    return parse_expression(raw, self._config)

  def run(self, history: HistoryManager):
    print("REPL Calculator — type 'help' for commands or 'exit' to quit.")
    while True:
      try:
        raw = input("> ").strip()
      except (KeyboardInterrupt, EOFError):
        print("\nGoodbye.")
        break

      if not raw:
        continue

      lowered = raw.lower()
      if lowered == "exit":
        print("Goodbye.")
        break
      if lowered == "help":
        _print_help()
        continue
      if lowered == "history":
        print(history.display())
        continue
      if lowered == "clear":
        history.clear()
        print("History cleared.")
        continue
      if lowered == "undo":
        if history.undo():
          print("Undone.")
        else:
          print("Nothing to undo.")
        continue
      if lowered == "redo":
        if history.redo():
          print("Redone.")
        else:
          print("Nothing to redo.")
        continue

      try:
        if is_chain_expression(raw):
          a, op_name, b = parse_chain_expression(raw, self._last_result, self._config)
        else:
          a, op_name, b = self._evaluate(raw)
        result = OperationFactory.execute(op_name, a, b)
        self._last_result = result
        self.notify_observers(CalculationEvent(op_name, a, b, result))
        print(result if result != int(result) else int(result))
      except CalculatorError as exc:
        print(f"Error: {exc}")

def run():
  """Wire up each observer and start the REPL"""
  config = CalculatorConfig()
  history = HistoryManager()
  logger = CalculatorLogger()

  runner = ReplLoop(config)
  runner.add_observer(history)
  runner.add_observer(logger)
  runner.run(history)
