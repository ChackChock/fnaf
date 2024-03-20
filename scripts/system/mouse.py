"""This module provides functionalities related to mouse interactions in a 2D
environment.

Classes:
    - MouseWheelStates: An enumeration class representing states of mouse wheel
    scrolling.
    - MouseButtonStates: An enumeration class representing states of a mouse button.
    - MouseButton: A data class representing a mouse button with a number and state.

Functions:
    - get_coords() -> pygame.Vector2: Returns the current mouse cursor coordinates.
    - get_prev_coords() -> pygame.Vector2: Returns the previous mouse cursor coordinates.
    - get_button(num: int) -> MouseButton: Returns the MouseButton object for a specified button
    number.
    - get_wheel() -> MouseWheelStates: Returns the current state of the mouse wheel.
    - motion() -> bool: Returns if there has been mouse motion since the last update.

Notes:
    - Advised not to use functions `update`, `press_button`, `release_button`,
    `scroll_wheel_up`, `scroll_wheel_down` and `move` because they are necessary for
    the correct operation of the module and are called in the App class (module
    scripts/system/app.py)
"""

__all__ = [
    "MouseWheelStates",
    "MouseButtonStates",
    "MouseButton",
    "get_coords",
    "get_prev_coords",
    "get_button",
    "get_wheel",
    "motion",
]


from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING, List, Optional

import pygame

if TYPE_CHECKING:
    from ..gui.widget import Widget

from . import display


class MouseWheelStates(IntEnum):
    """An enumeration class representing states of mouse wheel scrolling.

    Attributes:
        NO_STATE: Wheel is not scrolled up or scrolled down
        UP: Wheel is scrolled up
        DOWN: Wheel is scrolled down
    """

    NO_STATE = 0
    """Wheel is not scrolled up or scrolled down"""

    UP = 1
    """Wheel is scrolled up"""

    DOWN = 2
    """Wheel is scrolled down"""


class MouseButtonStates(IntEnum):
    """An enumeration class representing states of a mouse button.

    Attributes:
        NO_STATE: Button is not pressed, held or released
        PRESS: Button is pressed
        HOLD: Button is held
        RELEASE: Button is released
    """

    NO_STATE = 0
    """Button is not pressed, held or released"""

    PRESS = 1
    """Button is pressed"""

    HOLD = 2
    """Button is held"""

    RELEASE = 3
    """Button is released"""


@dataclass
class MouseButton:
    """A data class representing a mouse button with a number and state.

    Attributes:
        num: The number assigned to the mouse button.
        state: The state of the mouse button. Defaults to NO_STATE.
    """

    num: int
    """The number assigned to the mouse button."""
    state: MouseButtonStates = MouseButtonStates.NO_STATE
    """The state of the mouse button."""

    def copy(self) -> "MouseButton":
        """Creates copy of the current MouseButton object.

        Returns:
            MouseButton: A new instance of MouseButton with the same 'num' and 'state'
            as the original object.
        """
        return MouseButton(self.num, self.state)


@dataclass
class __Mouse:
    coords: pygame.Vector2 = field(default_factory=pygame.Vector2)
    prev_coords: pygame.Vector2 = field(default_factory=pygame.Vector2)
    motion: bool = False
    wheel: MouseWheelStates = MouseWheelStates.NO_STATE
    buttons: List[MouseButton] = field(
        default_factory=lambda: [MouseButton(i) for i in range(1, 4)]
    )
    interacted_widgets: List["Widget"] = field(default_factory=list)
    hovered_widgets: List["Widget"] = field(default_factory=list)
    default_cursor: pygame.Cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_ARROW)


def get_interacted_widgets() -> List["Widget"]:
    return __mouse.interacted_widgets.copy()


def get_hovered_widgets() -> List["Widget"]:
    return __mouse.hovered_widgets.copy()


def get_default_cursor() -> pygame.Cursor:
    return __mouse.default_cursor


def set_default_cursor(cursor: pygame.Cursor) -> None:
    __mouse.default_cursor = cursor


def get_coords() -> pygame.Vector2:
    """Returns the current mouse cursor coordinates as a pygame Vector2 object.

    Returns:
        pygame.Vector2: The current mouse cursor coordinates.
    """
    return __mouse.coords.copy()


def get_prev_coords() -> pygame.Vector2:
    """Returns the previous mouse cursor coordinates as a pygame Vector2 object.

    Returns:
        pygame.Vector2: The previous mouse cursor coordinates.
    """
    return __mouse.prev_coords.copy()


def get_button(num: int) -> MouseButton:
    """Returns a copy of the MouseButton object associated with the specified button
    number.

    Parameters:
        num (int): The button number (1, 2, or 3).

    Returns:
        MouseButton: A copy of the MouseButton object for the specified button number.

    Raises:
        ValueError: If the 'num' parameter is not within the range of 1 to 3.
    """
    if not 1 <= num <= 3:
        raise ValueError(
            f"The `num` argument can only accept integers from 1 to 3, given: {num}"
        )
    return __mouse.buttons[num - 1].copy()


def get_wheel() -> MouseWheelStates:
    """Returns the current state of the mouse wheel.

    Returns:
        MouseWheelStates: The current state of the mouse wheel.
    """
    return __mouse.wheel


def motion() -> bool:
    """Returns a boolean value indicating if there has been mouse motion since the last
    update.

    Returns:
        bool: True if there has been mouse motion, False otherwise.
    """
    return __mouse.motion


def update() -> None:
    """Updates the mouse coordinates, wheel state, and button states."""
    cursor: Optional[pygame.Cursor] = None

    for widget in __mouse.interacted_widgets:
        if cursor is not None:
            break
        cursor = widget.get_cursor()
    for widget in __mouse.hovered_widgets:
        if cursor is not None:
            break
        cursor = widget.get_cursor()

    if cursor:
        pygame.mouse.set_cursor(cursor)
    else:
        pygame.mouse.set_cursor(__mouse.default_cursor)

    __mouse.hovered_widgets.clear()
    __mouse.interacted_widgets.clear()
    __mouse.wheel = MouseWheelStates.NO_STATE
    __mouse.motion = False

    __mouse.prev_coords.update(__mouse.coords)
    __mouse.coords.update(pygame.mouse.get_pos())
    __mouse.coords.x *= display.get_surface_width() / display.get_display_width()
    __mouse.coords.y *= display.get_surface_height() / display.get_display_height()

    for button in __mouse.buttons:
        if button.state == MouseButtonStates.PRESS:
            button.state = MouseButtonStates.HOLD

        elif button.state == MouseButtonStates.RELEASE:
            button.state = MouseButtonStates.NO_STATE


def press_button(num: int) -> None:
    """Simulates pressing a mouse button based on the given button number.

    Parameters:
        num (int): The button number (1, 2, or 3).

    Raises:
        ValueError: If the 'num' parameter is not within the range of 1 to 3.
    """
    if not 1 <= num <= 3:
        raise ValueError(
            f"The `num` argument can only accept integers from 1 to 3, given: {num}"
        )
    __mouse.buttons[num - 1].state = MouseButtonStates.PRESS


def release_button(num: int) -> None:
    """Simulates releasing  a mouse button based on the given button number.

    Parameters:
        num (int): The button number (1, 2, or 3).

    Raises:
        ValueError: If the 'num' parameter is not within the range of 1 to 3.
    """
    if not 1 <= num <= 3:
        raise ValueError(
            f"The `num` argument can only accept integers from 1 to 3, given: {num}"
        )
    __mouse.buttons[num - 1].state = MouseButtonStates.RELEASE


def add_hovered_widgets(widget: "Widget") -> None:
    __mouse.hovered_widgets.append(widget)


def add_interacted_widgets(widget: "Widget") -> None:
    __mouse.interacted_widgets.append(widget)


def scroll_wheel_up() -> None:
    """Simulates scrolling the mouse wheel upwards."""
    __mouse.wheel = MouseWheelStates.UP


def scroll_wheel_down() -> None:
    """Simulates scrolling the mouse wheel downwards."""
    __mouse.wheel = MouseWheelStates.DOWN


def move() -> None:
    """Sets the flag to indicate that the mouse has moved."""
    __mouse.motion = True


__mouse = __Mouse()
