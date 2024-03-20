from typing import Optional

import pygame

from scripts.models import events
from scripts.system import display
from scripts.utils.timer import Timer
from scripts.windows import Window


class BaseWindow(Window):
    def __init__(self) -> None:
        super().__init__()

        self.__next_window_name: Optional[str] = None
        self.__timer = Timer(20, on_end_func=self.__process_timer_end)

    def __process_timer_end(self) -> None:
        if self.__next_window_name is not None:
            pygame.event.post(
                pygame.Event(events.CHANGE_WINDOW, name=self.__next_window_name)
            )
            self.__next_window_name = None

    def _set_timer_interval(self, interval: int) -> None:
        self.__timer.interval = interval

    def _start_window_change(self, name: str) -> None:
        self.__next_window_name = name
        self.__timer.start()

    def load(self) -> None:
        self.__timer.start()

    def render(self) -> None:
        super().render()

        if self.__timer.works:
            mult = self.__timer.ticks / self.__timer.interval
            if self.__next_window_name is None:
                a = int(mult * 255)
            else:
                a = int((1 - mult) * 255)
            display.get_surface().fill((a, a, a), special_flags=pygame.BLEND_RGB_MULT)

        self.__timer.update()
