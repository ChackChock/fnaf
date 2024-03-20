"""Module representing a font manager using Pygame.

This module provides functions to load, delete, render text using fonts, and get keys
in a dictionary.

Functions:
    - load(key: str, size: int, *paths: str) -> None: Load font from given path(s) for
    the specified key.
    - delete(key: str) -> None: Delete font data for the specified key.
    - render(key: str, text: str, antialias: bool, color: ColorValue, bgcolor:
    Optional[ColorValue] = None, wraplength: int = 0) -> pygame.Surface: Render text
    using the font associated with the key.
    - get_keys() -> Tuple[str, ...]: Get a tuple of all keys stored in the data.
    - get_font(key: str) -> Optional[pygame.Font]: Retrieve a pygame font object
    corresponding to the provided key
"""

from typing import Dict, Optional, Tuple

import pygame

from ..utils.file_functions import get_path
from ..models.types import ColorValue


def load(key: str, size: int, *paths: str) -> None:
    """Load font from the given path(s) for the specified key if it doesn't already
    exist in the data.

    Args:
        key (str): The key to access the font.
        size (int): The size of the font.
        *paths (str): Variable number of paths to search for the font files.

    Raises:
        KeyError: If the key already exists.
    """
    if key in __data:
        raise KeyError(f"The key `{key}` already exists!")
    __data[key] = pygame.Font(get_path(*paths), size)


def delete(key: str) -> None:
    """Delete the font data for the specified key if it exists in the data.

    Args:
        key (str): The key to delete from the data.

    Raises:
        KeyError: If the key does not exist or if the key is 'system'.
    """
    if key not in __data:
        raise KeyError(f"The key {key} does not exist!")
    if key == "system":
        raise KeyError("The key 'system' is already exists!")
    __data.pop(key)


def render(
    key: str,
    text: str,
    antialias: bool,
    color: ColorValue,
    bgcolor: Optional[ColorValue] = None,
    wraplength: int = 0,
) -> pygame.Surface:
    """Render text using the font associated with the given key.

    Args:
        key (str): The key associated with the font to use for rendering.
        text (str): The text to render.
        antialias (bool): Whether to use antialiasing.
        color (ColorValue): The color of the text.
        bgcolor (Optional[ColorValue]): The background color for the text (default is
        None).
        wraplength (int): The maximum width for text wrapping (default is 0).

    Returns:
        pygame.Surface: The rendered text as a pygame surface.
    """
    return __data[key].render(text, antialias, color, bgcolor, wraplength)


def get_keys() -> Tuple[str, ...]:
    """Get a tuple of all keys of stored fonts.

    Returns:
        Tuple[str, ...]: A tuple containing all keys present in the data.
    """
    return tuple(__data.keys())


def get_font(key: str) -> Optional[pygame.Font]:
    """Retrieve a pygame font object corresponding to the provided key.

    Args:
        key (str): The key representing the font to retrieve.

    Returns:
        Optional[pygame.Font]: A pygame font object associated with the key if found,
        otherwise None.
    """
    return __data.get(key)


__data: Dict[str, pygame.Font] = {}
__data["system"] = pygame.font.SysFont("Arial", 16)
