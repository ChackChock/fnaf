import pygame

from scripts import gui
from scripts.system import cursors, display

from .base_window import BaseWindow


class MenuWindow(BaseWindow):
    name = "menu"

    def _build(self):
        main_layout = gui.FloatLayout(0)

        layout = gui.VerticalLayout(display.get_surface_center(), 10)
        layout.add(
            [
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Подключиться", "main"),
                    click_listener=lambda w, e: self._start_window_change(
                        "client-room"
                    ),
                ),
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Создать комнату", "main"),
                    click_listener=lambda w, e: self._start_window_change(
                        "server-room"
                    ),
                ),
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Выйти", "main"),
                    click_listener=lambda w, e: pygame.event.post(
                        pygame.Event(pygame.QUIT)
                    ),
                ),
            ]
        )

        main_layout.add([layout])

        return main_layout

    def load(self) -> None:
        super().load()
        display.set_clear_color((255, 255, 255))
