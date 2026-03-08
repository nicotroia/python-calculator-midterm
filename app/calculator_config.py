"""Calculator configuration loaded from environment variables."""
import os
from dataclasses import dataclass, field
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

def _bool_env(key: str, default: bool) -> bool:
  """Read an env var as a boolean (true/1/yes is true, otherwise false)."""
  raw = os.getenv(key)
  if raw is None:
    return default
  return raw.strip().lower() in ("true", "1", "yes")

@dataclass
class CalculatorConfig:
  """Configuration class for the calculator.

  All values are read from environment variables (or a .env file)
  with sensible defaults.
  """
  # Directories
  log_dir: str = field(
    default_factory=lambda: os.getenv("CALCULATOR_LOG_DIR", "logs")
  )
  history_dir: str = field(
    default_factory=lambda: os.getenv("CALCULATOR_HISTORY_DIR", "logs")
  )

  # History settings
  max_history_size: int = field(
    default_factory=lambda: int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "0"))
  )  # 0 = unlimited
  auto_save: bool = field(
    default_factory=lambda: _bool_env("CALCULATOR_AUTO_SAVE", True)
  )

  # Calculation settings
  precision: int = field(
    default_factory=lambda: int(os.getenv("CALCULATOR_PRECISION", "10"))
  )
  max_input_value: Decimal = field(
    default_factory=lambda: Decimal(
      os.getenv("CALCULATOR_MAX_INPUT_VALUE", os.getenv("MAX_INPUT_VALUE", "1e10"))
    )
  )
  default_encoding: str = field(
    default_factory=lambda: os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
  )
