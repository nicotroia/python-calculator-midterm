# Python Calculator — IS601 Midterm

A command-line calculator built in Python. It supports standard arithmetic, a persistent history with undo/redo, chained calculations, and logging. Configurable via optional `.env` file

## Features

- Basic arithmetic: add, subtract, multiply, divide, power, root, modulus, integer division, percentage, absolute difference
- Word-style input (`add 5 3`) and infix expressions (`5 + 3`)
- Chain expressions — type just `* 2` to reuse the last result as the first operand
- Undo and redo for your calculation history
- History saved to CSV via pandas
- Structured CSV logging per day
- Configurable via environment variables

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.sample` to `.env` and adjust values as needed:

```bash
cp .env.sample .env
```

The available settings are:

| Variable                      | Default | Description                         |
| ----------------------------- | ------- | ----------------------------------- |
| `CALCULATOR_LOG_DIR`          | `logs`  | Where daily log files are written   |
| `CALCULATOR_HISTORY_DIR`      | `logs`  | Where history CSVs are saved        |
| `CALCULATOR_MAX_HISTORY_SIZE` | `0`     | Max history entries (0 = unlimited) |
| `CALCULATOR_AUTO_SAVE`        | `true`  | Auto-save history on exit           |
| `CALCULATOR_PRECISION`        | `10`    | Decimal places for results          |
| `CALCULATOR_MAX_INPUT_VALUE`  | `1e10`  | Largest accepted input number       |
| `CALCULATOR_DEFAULT_ENCODING` | `utf-8` | Encoding for file operations        |

## Usage

Start the REPL:

```bash
python main.py
```

Once running, you can type expressions or commands:

```
> 10 + 5        # infix expression → 15
> multiply 3 4  # word-style       → 12
> * 2           # chain: 12 * 2   → 24
> history       # show all past calculations
> undo          # revert last calculation
> redo          # re-apply undone calculation
> clear         # clear history
> help          # list all commands
> exit          # quit
```

Supported operators: `+`, `-`, `*`, `/`, `**`, `//`, `%`

## Running Tests

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=app tests/ --cov-report=term-missing
```

The project targets 90% coverage and the CI pipeline enforces this with `--cov-fail-under=90`.
