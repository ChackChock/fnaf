from typing import Dict, Optional, Tuple

import pygame

from ..models.types import ColorValue, Sequence
from ..utils.surface_functions import load_image


def get_cursor(key: str) -> pygame.Cursor:
    return __cursors[key]


def load_cursor(
    *paths: str,
    key: str,
    hotspot: Sequence[int],
    size: Optional[Tuple[int, int]] = None,
    colorkey: ColorValue = (0, 0, 0),
) -> None:
    __cursors[key] = pygame.Cursor(
        hotspot, load_image(*paths, size=size, colorkey=colorkey)
    )


__cursors: Dict[str, pygame.Cursor] = {}
