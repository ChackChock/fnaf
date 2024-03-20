import os
from typing import Optional, Tuple

import pygame

from ..models.types import ColorValue


def load_image(
    *paths: str,
    size: Optional[Tuple[int, int]] = None,
    colorkey: ColorValue = (0, 0, 0),
) -> pygame.Surface:
    path = os.path.join(*paths)

    if not os.path.exists(path):
        raise FileExistsError(f"File `{path}` does not exists!")
    if not os.path.isfile(path):
        raise ValueError(f"File `{path}` is not file!")

    try:
        image = pygame.image.load(path).convert()
    except Exception as e:
        e.add_note(f"Unexpected error while image `{path}` downloading.")
        raise e

    if size is not None:
        image = pygame.transform.scale(image, size)
    image.set_colorkey(colorkey)

    return image
