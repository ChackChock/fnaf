import pygame

from scripts.system import display

from .. import network

from .base_window import BaseWindow


class GameWindow(BaseWindow):
    name = "game"

    def load(self) -> None:
        super().load()
        display.set_clear_color((255, 255, 255))

        pygame.display.set_caption(str(network.get_mode()))

    def update(self) -> None:
        super().update()
