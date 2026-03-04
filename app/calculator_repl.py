"""Interactive REPL for the calculator."""
from app.exceptions import CalculatorError
from app.input_validators import parse_expression, OPERATOR_SYMBOLS
from app.operations import OperationFactory

# Each entry to be shown in help
COMMANDS = {
  "help": "Show this help message",
  "exit": "Quit the calculator",
}

# Human-readable label for each operator symbol used in help
_OP_HELP = " | ".join(
  f"'{sym}' ({name})" for sym, name in OPERATOR_SYMBOLS.items()
)

def _print_help():
  print("\n== Calculator Help ==")
  print("Enter an expression:  <number> <operator> <number>")
  print(f"  Operators: {_OP_HELP}")
  print("\nCommands:")
  for name, description in COMMANDS.items():
    print(f"  {name:<16} {description}")
  print()

def run():
  """Start the calculator REPL. Exits on 'exit' command or Ctrl+C."""
  print("Calculator REPL — type 'help' for commands or 'exit' to quit.")
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

    try:
      a, op_name, b = parse_expression(raw)
      result = OperationFactory.execute(op_name, a, b)
      # Show as int when result is a whole number
      print(result if result != int(result) else int(result))
    except CalculatorError as exc:
      print(f"Error: {exc}")
