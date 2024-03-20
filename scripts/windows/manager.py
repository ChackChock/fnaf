"""Module providing functions to manage windows and events in a pygame application.

Functions:
- create_window(window: Type[Window], name: str) -> None: Creates a new window with the specified name using the provided window class.
- change_window(name: str) -> None: Changes the current window to the window with the specified name.
- process_event(event: pygame.Event) -> None: Processes the given event in the current window.
- update() -> None: Updates the current window if it exists.
- render() -> None: Renders the contents of the current window.
"""

__all__ = [
    "get_window",
    "create_window",
    "process_event",
    "update",
    "render",
]


from dataclasses import dataclass, field
from typing import Dict, Optional, Type

import pygame

from ..models.events import CHANGE_WINDOW

from .window import Window
from ..models.exceptions import (
    NoWindowError,
    WindowAlreadyExistsError,
    WindowNotFoundError,
)


@dataclass
class __WindowsData:
    windows: Dict[str, Window] = field(default_factory=dict)
    current_window: Optional[Window] = None


def __change_window(name: str) -> None:
    """Changes the current window to the window with the specified name.

    Args:
        name (str): The name of the window to change to.

    Raises:
        WindowNotFoundError: If the specified window is not found in the windows data.
        NoWindowError: If there is no current window set.
    """
    if name not in __windows_data.windows:
        raise WindowNotFoundError(
            f"Window with name `{name}` is not found! Existing windows: "
            + "".join(
                [
                    f"{_name}: {window.__class__.__name__}"
                    for _name, window in __windows_data.windows.items()
                ]
            )
        )
    if __windows_data.current_window is None:
        raise NoWindowError("No one window has been created!")
    __windows_data.current_window.clear()
    __windows_data.current_window = __windows_data.windows[name]
    __windows_data.current_window.load()

    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))


def get_window(name: str) -> Window:
    if name not in __windows_data.windows:
        raise WindowAlreadyExistsError(
            f"Window with name `{name}` already exists: {__windows_data.windows[name].__class__.__name__} has name {name}!"
        )
    return __windows_data.windows[name]


def get_current_window() -> Window:
    if __windows_data.current_window is None:
        raise NoWindowError("No one window has been created!")
    return __windows_data.current_window


def create_window(window: Type[Window]) -> None:
    """Creates a window and adds it to the window registry. If there is already a window
    with the same name, a WindowAlreadyExistsError will be raised.

    Args:
        window (Type[Window]): The window class to create and add to the registry.

    Raises:
        WindowAlreadyExistsError: If a window with the same name already exists in the
        registry.
    """
    if window.name in __windows_data.windows:
        raise WindowAlreadyExistsError(
            f"Window with name `{window.name}` already exists: {__windows_data.windows[window.name].__class__.__name__} has name {window.name}!"
        )
    __windows_data.windows[window.name] = window()
    if __windows_data.current_window is None:
        __windows_data.current_window = __windows_data.windows[window.name]
        __windows_data.current_window.load()


def process_event(event: pygame.Event) -> None:
    """Processes the given event in the current window.

    Args:
        event (pygame.Event): The event to process.

    Raises:
        NoWindowError: If there is no current window set.
    """
    if __windows_data.current_window is None:
        raise NoWindowError("No one window has been created!")
    if event.type == CHANGE_WINDOW:
        __change_window(event.name)
    else:
        __windows_data.current_window.process_event(event)


def update() -> None:
    """Updates the current window if it exists.

    Raises:
        NoWindowError: If there is no current window set.
    """
    if __windows_data.current_window is None:
        raise NoWindowError("No one window has been created!")
    __windows_data.current_window.update()


def render() -> None:
    """Renders the contents of the current window.

    Raises:
        NoWindowError: If there is no current window set.
    """
    if __windows_data.current_window is None:
        raise NoWindowError("No one window has been created!")
    __windows_data.current_window.render()


__windows_data = __WindowsData()
