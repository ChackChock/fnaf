"""Module to manage keyboard key states.

Classes:
    - KeyStates: An enumeration class representing states of a keyboard key.

Functions:
    - get_key(): Get the state of a specific key.
    - get_keys(): Get the states of multiple keys.
    - get_pressed_keys(): Get the dictionary containing currently pressed keys mapped
    to their states.

Notes:
    - Advised not to use functions `update`, `press_key` and `release_key` because they
    are necessary for the correct operation of the module and are called in the App
    class (module scripts/system/app.py)
"""


__all__ = [
    "KeyStates",
    "get_key",
    "get_keys",
    "get_pressed_keys",
]


from typing import Dict, List
from enum import IntEnum


class KeyStates(IntEnum):
    """An enumeration class representing states of a keyboard key.

    Attributes:
        NO_STATE: Key is not pressed, held, or released.
        PRESS: Key is pressed.
        HOLD: Key is held.
        RELEASE: Key is released.
    """

    NO_STATE = 0
    """Key is not pressed, held or released"""

    PRESS = 1
    """Key  is pressed"""

    HOLD = 2
    """Key  is held"""

    RELEASE = 3
    """Key  is released"""


def get_key(key: int) -> KeyStates:
    """Get the state of a specific key.

    Args:
        key (int): The key to get the state for.

    Returns:
        KeyStates: The state of the key, defaulting to KeyStates.NO_STATE if not found.
    """
    return __keys.get(key, KeyStates.NO_STATE)


def get_keys(*keys: int) -> List[KeyStates]:
    """Get the states of multiple keys.

    Args:
        *keys (int): Variable number of keys to get the states for.

    Returns:
        List[KeyStates]: A list of states corresponding to the input keys.
    """
    return [get_key(key) for key in keys]


def get_pressed_keys() -> Dict[int, KeyStates]:
    """Get the dictionary containing currently pressed keys mapped to their states.

    Returns:
        Dict[int, KeyStates]: The dictionary with keys and their states."""
    return __keys.copy()


def update() -> None:
    """Update the states of keys, transitioning from PRESS to HOLD and removing RELEASED
    keys.
    """
    for key, state in list(__keys.items()):
        if state == KeyStates.PRESS:
            __keys[key] = KeyStates.HOLD
        elif state == KeyStates.RELEASE:
            __keys.pop(key)


def press_key(key: int) -> None:
    """Simulate pressing a key by updating its state to KeyStates.PRESS.

    Args:
        key (int): The key to press.
    """
    __keys[key] = KeyStates.PRESS


def release_key(key: int) -> None:
    """Simulate releasing a key by updating its state to KeyStates.RELEASE.

    Args:
        key (int): The key to release.
    """
    __keys[key] = KeyStates.RELEASE


__keys: Dict[int, KeyStates] = dict()
