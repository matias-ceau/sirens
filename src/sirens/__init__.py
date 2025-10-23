"""French emergency vehicle siren simulator.

Generate, play, and manipulate realistic siren sounds.
"""

__version__ = "0.1.0"

from .core import Siren
from .presets import PRESETS, register_custom_siren, get_available_sirens
from .cli import main

__all__ = [
    "Siren",
    "PRESETS",
    "register_custom_siren",
    "get_available_sirens",
    "main",
]
