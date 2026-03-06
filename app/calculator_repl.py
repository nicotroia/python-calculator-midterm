"""Interactive REPL for the calculator."""
from app.calculator_config import CalculatorConfig
from app.calculator_history import CalculatorHistory
from app.calculator_logs import CalculatorLogger
from app.exceptions import CalculatorError, ValidationError
from app.input_validators import (
  parse_expression, parse_word_command, OPERATOR_SYMBOLS, WORD_COMMANDS,
)
from app.observer import CalculationEvent, Observable
from app.operations import OperationFactory

# Each entry to be shown in help
COMMANDS = {
  "help":    "Show this help message",
  "history": "Display calculation history",
  "clear":   "Clear calculation history",
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


class _ReplRunner(Observable):
  """Runs the REPL loop and notifies observers of each calculation."""

  def __init__(self, config: CalculatorConfig):
    super().__init__()
    self._config = config

  def _evaluate(self, raw: str):
    """Try word-command first, fall back to infix expression."""
    try:
      return parse_word_command(raw, self._config)
    except ValidationError:
      pass
    return parse_expression(raw, self._config)

  def run(self, history: CalculatorHistory):
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

      try:
        a, op_name, b = self._evaluate(raw)
        result = OperationFactory.execute(op_name, a, b)
        self.notify_observers(CalculationEvent(op_name, a, b, result))
        print(result if result != int(result) else int(result))
      except CalculatorError as exc:
        print(f"Error: {exc}")


def run():
  """Entry point: wire observers and start the REPL."""
  config = CalculatorConfig()
  history = CalculatorHistory()
  logger = CalculatorLogger()

  runner = _ReplRunner(config)
  runner.add_observer(history)
  runner.add_observer(logger)
  runner.run(history)
