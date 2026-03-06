"""Calculator configuration loaded from environment variables."""
import os
from dataclasses import dataclass, field
from decimal import Decimal

from dotenv import load_dotenv

load_dotenv()

@dataclass
class CalculatorConfig:
  """Configuration class for the calculator.

  Values are read from environment variables (or .env) on first import 
  with basic defaults
  """
  max_input_value: Decimal = field(
    default_factory=lambda: Decimal(os.getenv("MAX_INPUT_VALUE", "1e10"))
  )
