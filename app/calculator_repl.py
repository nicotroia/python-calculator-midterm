"""Interactive REPL calculator"""
import readline  # enables up/down arrow history in input()
from colorama import init as colorama_init, Fore, Style
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

def _print_gradient(text: str) -> None:
  """Print text with a rainbow gradient using 256-color ANSI codes"""
  colors = [255, 253, 195, 189, 153, 117, 111, 105, 99, 63, 57, 93, 129, 135, 141, 147, 183]
  reset = "\033[0m"
  gradient = ""
  for i, ch in enumerate(text):
    code = colors[i % len(colors)]
    gradient += f"\033[38;5;{code}m{ch}"
  print(gradient + reset)

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
    print("Welcome to ", end="")
    _print_gradient("Nico's REPL Calculator")
    print("Type 'help' for commands or 'exit' to quit.")
    while True:
      try:
        raw = input("> ").strip()
      except (KeyboardInterrupt, EOFError):
        print()
        _print_gradient("Goodbye :)")
        break

      if not raw:
        continue

      lowered = raw.lower()
      if lowered == "exit":
        _print_gradient("Goodbye :)")
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
        display = result if result != int(result) else int(result)
        print(Fore.GREEN + str(display) + Style.RESET_ALL)
      except CalculatorError as exc:
        print(f"Error: {exc}")

def run():
  """Wire up each observer and start the REPL"""
  colorama_init(autoreset=True)
  config = CalculatorConfig()
  history = HistoryManager()
  logger = CalculatorLogger(config)

  runner = ReplLoop(config)
  runner.add_observer(history)
  runner.add_observer(logger)
  runner.run(history)
