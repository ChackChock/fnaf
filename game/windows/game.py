import pygame

from scripts import gui
from scripts.system import cursors, display

from .. import network

from .base_window import BaseWindow


class GameWindow(BaseWindow):
    name = "game"

    def _build(self):
        main_layout = gui.FloatLayout(0)

        layout = gui.VerticalLayout(display.get_surface_center(), 10)
        layout.add(
            [
                gui.Label(0, "", "main"),
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Отправить", "main"),
                    click_listener=lambda w, e: network.send_message(1)
                ),
            ]
        )

        main_layout.add([layout])

        return main_layout

    def load(self) -> None:
        super().load()
        display.set_clear_color((255, 255, 255))

        pygame.display.set_caption(str(network.get_mode()))

    def update(self) -> None:
        super().update()

        data = network.get_data()
        if data:
            print(data)
