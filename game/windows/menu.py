import pygame

from scripts import gui
from scripts.system import cursors, display

from .. import network

from .base_window import BaseWindow


class MenuWindow(BaseWindow):
    name = "menu"

    def __connect_to_room(self) -> None:
        network.start_client()
        self._start_window_change("game")

    def __create_room(self) -> None:
        network.start_server()
        self._start_window_change("game")

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
                    click_listener=lambda w, e: self.__connect_to_room(),
                ),
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Создать комнату", "main"),
                    click_listener=lambda w, e: self.__create_room(),
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
