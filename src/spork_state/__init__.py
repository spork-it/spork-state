"""Thread-safe state management for Spork and Python."""

from importlib.metadata import PackageNotFoundError, version
from typing import Any

from .core import (
    Atom,
    add_watch,
    atom as _spork_atom,
    atom_q,
    compare_and_set,
    deref,
    get_validator,
    remove_watch,
    reset,
    reset_vals,
    set_validator,
    subscribe,
    swap,
    swap_vals,
    validation_error_message,
)

VALIDATION_ERROR_MESSAGE = validation_error_message


def atom(value: Any, validator: Any = None) -> Atom:
    """Create an :class:`Atom`, optionally guarded by ``validator``."""
    if validator is None:
        return _spork_atom(value)
    return _spork_atom(value, validator)


def is_atom(value: Any) -> bool:
    """Return whether ``value`` is an :class:`Atom`."""
    return atom_q(value)


try:
    __version__ = version("spork-state")
except PackageNotFoundError:  # Source-tree and direct build-output imports.
    __version__ = "0.1.0"


__all__ = [
    "Atom",
    "VALIDATION_ERROR_MESSAGE",
    "add_watch",
    "atom",
    "compare_and_set",
    "deref",
    "get_validator",
    "is_atom",
    "remove_watch",
    "reset",
    "reset_vals",
    "set_validator",
    "subscribe",
    "swap",
    "swap_vals",
    "__version__",
]
