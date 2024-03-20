"""This module provides functionalities to manage the display settings and rendering
in Pygame.

Functions:
    - get_display_surface() -> pygame.Surface: Returns the display surface in Pygame.
    - get_display_rect() -> pygame.Rect: Returns a copy of the display rectangle in
    Pygame.
    - get_display_center() -> Tuple[int, int]: Returns the coordinates of the center
    of the display rectangle in Pygame.
    - get_display_size() -> Tuple[int, int]: Returns the size of the display rectangle
    in Pygame.
    - get_display_width() -> int: Returns the width of the display rectangle in Pygame.
    - get_display_height() -> int: Returns the height of the display rectangle in
    Pygame.
    - get_surface() -> pygame.Surface: Returns the surface in Pygame.
    - get_surface_rect() -> pygame.Rect: Returns a copy of the surface rectangle in
    Pygame.
    - get_surface_center() -> Tuple[int, int]: Returns the coordinates of the center
    of the surface rectangle in Pygame.
    - get_surface_size() -> Tuple[int, int]: Returns the size of the surface rectangle
    in Pygame.
    - get_surface_width() -> int: Returns the width of the surface rectangle in Pygame.
    - get_surface_height() -> int: Returns the height of the surface rectangle in
    Pygame.
    - get_clear_color() -> ColorValue: Returns the clear color value.
    - set_clear_color(color: ColorValue) -> None: Sets the clear color value.

Notes:
    - Advised not to use functions `init`, `clear` and `render` because they are
    necessary for the correct operation of the module and are called in the App class
    (module scripts/system/app.py)
"""

__all__ = [
    "get_display_surface",
    "get_display_rect",
    "get_display_center",
    "get_display_size",
    "get_display_width",
    "get_display_height",
    "get_surface",
    "get_surface_rect",
    "get_surface_center",
    "get_surface_size",
    "get_surface_width",
    "get_surface_height",
    "get_clear_color",
    "set_clear_color",
]


from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple

import pygame

from ..models.exceptions import DisplayInitializedError
from ..models.types import ColorValue, Coordinate
from ..utils.surface_functions import load_image


@dataclass
class __DisplayData:
    display: Optional[pygame.Surface] = None
    display_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    surface: Optional[pygame.Surface] = None
    surface_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    clear_color: ColorValue = (0, 0, 0)


def init(
    display_size: Coordinate,
    surface_size: Coordinate,
    flags: int = 0,
    caption: str = "",
    icon: Optional[Sequence[str]] = None,
    clear_color: ColorValue = (0, 0, 0),
) -> None:
    """Initializes the display window with the specified parameters.

    Args:
        display_size (Coordinate): The size of the display window as a tuple (width,
        height).
        surface_size (Coordinate): The size of the surface inside the display window
        as a tuple (width, height).
        flags (int, optional): Additional flags for configuring the pygame window.
        Defaults to 0.
        caption (str, optional): The window title. Defaults to "".
        icon (Optional[pygame.Surface], optional): The window icon. Defaults to None.
        clear_color (ColorValue, optional): The background color of the window in RGB
        format. Defaults to (0, 0, 0).

    Example:
        init(display_size=(800, 600), surface_size=(640, 480), caption="My Game Window",
        icon=my_icon_surface, clear_color=(255, 255, 255))
    """
    __data.display = pygame.display.set_mode(pygame.Vector2(display_size), flags)
    __data.display_rect = __data.display.get_rect()
    __data.surface = pygame.Surface(pygame.Vector2(surface_size))
    __data.surface_rect = __data.surface.get_rect()
    __data.clear_color = clear_color

    if icon:
        pygame.display.set_icon(load_image(*icon))
    pygame.display.set_caption(caption)


# Display
def get_display_surface() -> pygame.Surface:
    """Returns the pygame display surface.

    Returns:
        pygame.Surface: The display surface.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display


def get_display_rect() -> pygame.Rect:
    """Returns a copy of the display rectangle in Pygame.

    Returns:
        pygame.Rect: A copy of the display rectangle.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display_rect.copy()


def get_display_center() -> Tuple[int, int]:
    """Returns the coordinates of the center of the display rectangle in Pygame.

    Returns:
        Tuple[int, int]: The coordinates of the center (x, y).

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display_rect.center


def get_display_size() -> Tuple[int, int]:
    """Returns the size of the display rectangle in Pygame.

    Returns:
        Tuple[int, int]: The size of the display rectangle (width, height).

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display_rect.size


def get_display_width() -> int:
    """Returns the width of the display rectangle in Pygame.

    Returns:
        int: The width of the display rectangle.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display_rect.width


def get_display_height() -> int:
    """Returns the height of the display rectangle in Pygame.

    Returns:
        int: The height of the display rectangle.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.display_rect.height


# Surface
def get_surface() -> pygame.Surface:
    """Returns the surface in Pygame.

    Returns:
        pygame.Surface: The surface object.

    Raises:
        DisplayInitializedError: If the surface has not been initialized.
    """
    if __data.surface is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface


def get_surface_rect() -> pygame.Rect:
    """Returns a copy of the surface rectangle in Pygame.

    Returns:
        pygame.Rect: A copy of the surface rectangle.

    Raises:
        DisplayInitializedError: If the surface has not been initialized.
    """
    if __data.surface is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface_rect.copy()


def get_surface_center() -> Tuple[int, int]:
    """Returns the coordinates of the center of the surface rectangle in Pygame.

    Returns:
        Tuple[int, int]: The coordinates of the center (x, y).

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface_rect.center


def get_surface_size() -> Tuple[int, int]:
    """Returns the size of the surface rectangle in Pygame.

    Returns:
        Tuple[int, int]: The size of the surface rectangle (width, height).

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface_rect.size


def get_surface_width() -> int:
    """Returns the width of the surface rectangle in Pygame.

    Returns:
        int: The width of the surface rectangle.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface_rect.width


def get_surface_height() -> int:
    """Returns the height of the surface rectangle in Pygame.

    Returns:
        int: The height of the surface rectangle.

    Raises:
        DisplayInitializedError: If the display has not been initialized.
    """
    if __data.display is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    return __data.surface_rect.height


# Other
def get_clear_color() -> ColorValue:
    """Returns the clear color value.

    Returns:
        ColorValue: The clear color value.
    """
    return __data.clear_color


def set_clear_color(color: ColorValue) -> None:
    """Sets the clear color value.

    Parameters:
        color (ColorValue): The new color value to set.
    """
    __data.clear_color = color


def clear() -> None:
    """Clears the display and surface with the specified clear color.

    Raises:
        DisplayInitializedError: If the display or surface has not been initialized.
    """
    if __data.display is None or __data.surface is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    __data.display.fill(__data.clear_color)
    __data.surface.fill(__data.clear_color)


def render() -> None:
    """Renders the scaled surface onto the display and updates the display.

    Raises:
        DisplayInitializedError: If the display or surface has not been initialized.
    """
    if __data.display is None or __data.surface is None:
        raise DisplayInitializedError(
            "module scripts\\system\\display.py has not been initialized!"
        )
    scaled_surface = pygame.transform.scale(__data.surface, __data.display_rect.size)
    __data.display.blit(scaled_surface, (0, 0))
    pygame.display.update()


__data = __DisplayData()
