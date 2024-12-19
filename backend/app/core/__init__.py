"""
Core module initialization file for the StockSense backend application.
This module contains core functionality and configurations that are used throughout the application.
"""

from pathlib import Path
import sys

# Add the parent directory to sys.path to enable relative imports
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Version information
__version__ = "1.0.0"
__author__ = "StockSense Team"

# Import core components for easier access
from .config import get_settings  # noqa: F401
from .security import get_password_hash, verify_password  # noqa: F401
from .database import get_db  # noqa: F401

# Define what should be imported when using "from core import *"
__all__ = [
    "get_settings",
    "get_password_hash",
    "verify_password",
    "get_db",
]