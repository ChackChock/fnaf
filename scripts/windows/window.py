"""Module representing a Window in a pygame application.

Classes:
    Window:
        Represents a window in a pygame application.

        Attributes:
            name (str): The name of the window.

        Methods:
            _build(self) -> Optional[gui.Widget]:
                Builds and returns the main layout of the window.

            process_event(self, event: pygame.Event) -> None:
                Processes the given event in the window.

            load(self) -> None:
                Loads necessary resources for the window.

            clear(self) -> None:
                Clears the contents of the window.

            update(self) -> None:
                Updates the window's main layout if it exists.

            render(self) -> None:
                Renders the contents of the window on the display surface.

Usage:
    import pygame

    from scripts import gui
    from scripts.windows.window import Window
    from scripts.windows import manager
    from scripts.system import display

    class MyWindow(Window):
        name = "MyWindow"
        def _build(self) -> gui.Widget:
            layout = gui.VerticalLayout(display.get_surface_center())
            layout.add([
                gui.Button(0, text="Start", click_func=lambda w, e: manager.change_window("game")),
                gui.Button(0, text="Exit", click_func=lambda w, e: pygame.event.post(pygame.Event(pygame.QUIT))),
            ])
            return layout

        def load(self) -> None:
            display.set_clear_color((255, 255, 255))

    manager.create_window(MyWindow)

"""

__all__ = ["Window"]


import pygame

from ..system import display
from .. import gui


class Window:
    """Represents a window in a pygame application.

    Attributes:
        name (str): The name of the window.

    Methods:
        _build(self) -> Optional[gui.Widget]: Builds and returns the main layout of the
        window.
        process_event(self, event: pygame.Event) -> None: Processes the given event in
        the window.
        load(self) -> None: Loads necessary resources for the window.
        clear(self) -> None: Clears the contents of the window.
        update(self) -> None: Updates the window's main layout if it exists.
        render(self) -> None: Renders the contents of the window on the display surface.
    """

    name: str

    def __init__(self) -> None:
        self.__main_layout = self._build()
        if not issubclass(type(self.__main_layout), gui.Container):
            raise ValueError(
                f"Method `_build` of {self} must retrun subclass of gui.Container, not {type(self.__main_layout)}"
            )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: name='{self.name}'>"

    @property
    def main_layout(self) -> gui.Container:
        return self.__main_layout

    def _build(self) -> gui.Container:
        """Builds and returns the main layout of the window.

        Returns:
            gui.Container: The main layout of the window.
        """
        raise NotImplementedError(f"Method `_build` of {self} must be implemented!")

    def process_event(self, event: pygame.Event) -> None:
        """Processes the given event in the window.

        Arguments:
            event (pygame.Event): The event to be processed.
        """
        ...

    def load(self) -> None:
        """Loads necessary resources for the window."""
        ...

    def clear(self) -> None:
        """Clears the contents of the window."""
        ...

    def update(self) -> None:
        """Updates the window's main layout if it exists."""
        if self.__main_layout is not None:
            self.__main_layout.update()

    def render(self) -> None:
        """Renders the contents of the window on the display surface."""
        if self.__main_layout is not None:
            self.__main_layout.render(display.get_surface())
