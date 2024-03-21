import pygame

from scripts import gui
from scripts.system import display

from .. import network

from .base_window import BaseWindow


class GameWindow(BaseWindow):
    name = "game"

    def _build(self) -> gui.Container:
        main_layout = gui.VerticalLayout(display.get_surface_center())
        self.__label = gui.Label(0, "", "main")

        main_layout.add(self.__label)

        return main_layout

    def load(self) -> None:
        super().load()
        display.set_clear_color((255, 255, 255))

        pygame.display.set_caption(str(network.get_mode()))

    def update(self) -> None:
        super().update()

        for data in network.get_data():
            if data["key"] == "deleting":
                self.__label.set_text("")
            elif data["data"] == "whitespace":
                self.__label.set_text(self.__label.get_text() + "\n")
            else:
                self.__label.set_text(self.__label.get_text() + data["data"])

    def process_event(self, event: pygame.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                network.send_message("deleting", None)
            elif event.key in (pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER):
                network.send_message("typing", "whitespace")
            else:
                network.send_message("typing", event.unicode)
