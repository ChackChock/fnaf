"""Module to manage the main application loop and event handling.

This module contains the `App` class responsible for managing the main application loop,
handling events, updating the application state, and rendering the application.
"""

__all__ = ["App"]


from typing import Any, Dict, Optional, Sequence, Union

from memory_profiler import memory_usage
import pygame

from . import display
from . import font
from . import keyboard
from . import mouse

from ..utils.file_functions import read_file
from ..utils import constants
from ..windows import manager


class App:
    """Class to manage the main application loop and event handling.

    Attributes:
        - __running (bool): Flag to control the main application loop.
        - __maxFPS (int): Maximum frames per second for the application.
        - __clock (pygame.time.Clock): Pygame clock object for controlling frame rate.

    Methods:
        - __init__(self) -> None: Initialize the application with optional settings
        loaded from a JSON file.
        - __handle_events(self) -> None: Handle Pygame events such as keyboard input
        and mouse actions.
        - __update(self) -> None: Update the application state.
        - __render(self) -> None: Render the application using a manager and display
        system.
        - run(self) -> None: Main application loop that handles events, updates, and
        renders the app.
    """

    def __init__(
        self, flags: int = 0, caption: str = "", icon: Optional[Sequence[str]] = None
    ) -> None:
        app_data: Union[Exception, Dict[str, Any]] = read_file(
            "data", "app-config.json", raise_exc=False
        )

        if isinstance(app_data, Exception):
            app_data = {}

        self.__running = True
        self.__f3_key_clicks = False
        self.__index = 0

        self.__maxFPS: int = app_data.get("max-fps", constants.MAX_FPS)
        self.__clock = pygame.time.Clock()

        display.init(
            app_data.get("display-size", constants.DISPLAY_SIZE),
            app_data.get("surface-size", constants.SURFACE_SIZE),
            flags,
            caption,
            icon,
        )

    def __handle_events(self) -> None:
        """Handle Pygame events such as keyboard input and mouse actions.

        This method checks and processes all Pygame events, updating the keyboard module
        and mouse module states accordingly.
        """
        keyboard.update()
        mouse.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button <= 3:
                    mouse.press_button(event.button)
            elif event.type == pygame.MOUSEMOTION:
                mouse.move()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button <= 3:
                    mouse.release_button(event.button)
                elif event.button == 4:
                    mouse.scroll_wheel_up()
                elif event.button == 5:
                    mouse.scroll_wheel_down()

            elif event.type == pygame.KEYDOWN:
                keyboard.press_key(event.key)
            elif event.type == pygame.KEYUP:
                keyboard.release_key(event.key)

            manager.process_event(event)

        if keyboard.get_key(pygame.K_F3) == keyboard.KeyStates.PRESS:
            self.__f3_key_clicks = (self.__f3_key_clicks + 1) % 4
            self.__index = 0
        if keyboard.get_key(pygame.K_KP_PLUS) == keyboard.KeyStates.PRESS:
            self.__index += 1
        if keyboard.get_key(pygame.K_KP_MINUS) == keyboard.KeyStates.PRESS:
            self.__index -= 1

    def __update(self) -> None:
        """Update the application state based on input events.

        This method calls the manager's update function to update the application state.
        """
        manager.update()

    def __render(self) -> None:
        """Render the application using the manager and display system.

        This method clears the display, calls the manager's render function, and renders
        the updated display.
        """
        display.clear()
        manager.render()

        if __debug__ and self.__f3_key_clicks:
            surface = display.get_surface()
            hovered_widgets = mouse.get_hovered_widgets()
            rect = pygame.Rect((0, 0), (0, 0))

            text = ""
            for index, widget in enumerate(hovered_widgets):
                if index == self.__index:
                    pygame.draw.rect(surface, (255, 50, 50), widget.get_absolute_rect(), 3)
                else:
                    pygame.draw.rect(surface, (50, 255, 50), widget.get_absolute_rect(), 1)
                text += f"{index:<6}: {widget}\n"
            if text:
                text = "layer: widget\n" + text

            if self.__f3_key_clicks in (1, 3):
                image = font.render("system", text, True, (1, 1, 1))
                rect = pygame.Rect(
                    (5, 5),
                    (image.get_width() + 10, image.get_height() + 10),
                )
                surface.fill((255, 255, 255), rect)
                surface.blit(image, image.get_rect(center=rect.center))
                pygame.draw.rect(surface, (1, 1, 1), rect, 1)

            if hovered_widgets and self.__f3_key_clicks <= 2:
                self.__index %= len(hovered_widgets)
                image = font.render(
                    "system",
                    f"layer: {self.__index}\n"
                    + hovered_widgets[self.__index].get_info(),
                    True,
                    (1, 1, 1),
                )
                rect = pygame.Rect(
                    (5, rect.bottom + 5),
                    (image.get_width() + 10, image.get_height() + 10),
                )
                surface.fill((255, 255, 255), rect)
                surface.blit(image, image.get_rect(center=rect.center))
                pygame.draw.rect(surface, (1, 1, 1), rect, 1)

            mpos = [round(x, 2) for x in mouse.get_coords()]
            pygame.draw.line(
                surface,
                (255, 50, 50),
                (mpos[0], 0),
                (mpos[0], display.get_surface_height()),
            )
            pygame.draw.line(
                surface,
                (255, 50, 50),
                (0, mpos[1]),
                (display.get_surface_width(), mpos[1]),
            )

            mem = round(memory_usage(interval=0, max_usage=True), 6)
            fps = round(self.__clock.get_fps(), 6)

            image = font.render(
                "system",
                f"fps: {fps}\nmemory(MiB): {mem}\nmouse coords: x={mpos[0]}, y={mpos[1]}",
                True,
                (1, 1, 1),
            )
            rect = pygame.Rect(
                (display.get_display_width() - image.get_width() - 15, 5),
                (image.get_width() + 10, image.get_height() + 10),
            )
            surface.fill((255, 255, 255), rect)
            surface.blit(image, image.get_rect(center=rect.center))
            pygame.draw.rect(surface, (1, 1, 1), rect, 1)

        display.render()

    def run(self) -> None:
        """Main application loop that handles events, updates, and renders the app.

        This method runs the main loop of the application.
        """
        while self.__running:
            self.__handle_events()
            self.__update()
            self.__render()

            self.__clock.tick(self.__maxFPS)
