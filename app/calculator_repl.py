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

# Maps operation name → first matching word alias (e.g. "absolute_difference" → "abs_diff")
_OP_TO_WORD: dict[str, str] = {}
for _word, _op in WORD_COMMANDS.items():
  if _op not in _OP_TO_WORD:
    _OP_TO_WORD[_op] = _word

def _print_gradient(text: str) -> None:
  """Print text with a colored gradient using 256-color ANSI codes"""
  colors = [99, 105, 111, 117, 123, 129, 153, 189, 195, 255, 253, 195, 183, 147, 141, 135, 129, 111]
  reset = "\033[0m"
  gradient = ""
  for i, ch in enumerate(text):
    code = colors[i % len(colors)]
    gradient += f"\033[38;5;{code}m{ch}"
  print(gradient + reset)

def _print_help():
  T = Fore.LIGHTCYAN_EX   # title color
  S = Fore.LIGHTBLACK_EX  # subtle color
  R = Style.RESET_ALL
  print(f"\n{T}== Calculator Help =={R}")
  print(f"\n{T}Infix:{R:<11}  <number> <operator> <number>")
  print(f"{S}Example:{R:<10} (1 + 2)")
  print(f"\n{T}Word:{R:<11}   <operation> <number> <number>")
  print(f"{S}Example:{R:<10} (add 1 2)")
  print(f"\n{T}Operators:{R}")
  for sym, name in OPERATOR_SYMBOLS.items():
    alias = _OP_TO_WORD.get(name, name)
    print(f"  {T}{sym:<12}{R} {alias}")
  print(f"\n{T}Commands:{R}")
  for name, description in COMMANDS.items():
    print(f"  {T}{name:<12}{R} {description}")
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
        print(Fore.LIGHTCYAN_EX + "Goodbye " + Style.RESET_ALL + Fore.LIGHTBLACK_EX + ":)" + Style.RESET_ALL)
        break

      if not raw:
        continue

      lowered = raw.lower()
      if lowered == "exit":
        print(Fore.LIGHTCYAN_EX + "Goodbye " + Style.RESET_ALL + Fore.LIGHTBLACK_EX + ":)" + Style.RESET_ALL)
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
