from typing import Any, Callable, Optional


class Timer:
    def __init__(
        self,
        interval: int,
        on_update_func: Optional[Callable[[int, int], Any]] = None,
        on_end_func: Optional[Callable[[], Any]] = None,
        loops: int = 1,
    ) -> None:
        self.__interval = interval
        self.__on_update_func = on_update_func
        self.__on_end_func = on_end_func
        self.__loops = loops
        self.__loop = loops

        self.__ticks = 0
        self.__ended = True
        self.__paused = False

    @property
    def works(self) -> bool:
        return not (self.__ended or self.__paused)

    @property
    def ended(self) -> bool:
        return self.__ended

    @property
    def paused(self) -> bool:
        return self.__paused

    @property
    def interval(self) -> int:
        return self.__interval

    @interval.setter
    def interval(self, value: int) -> None:
        self.__interval = value

    @property
    def ticks(self) -> int:
        return self.__ticks

    @property
    def loop(self) -> int:
        return self.__loop

    @property
    def loops(self) -> int:
        return self.__loops

    @loops.setter
    def loops(self, value: int) -> None:
        self.__loops = value

    def start(self) -> None:
        self.__ticks = 0
        self.__loop = self.__loops
        self.__ended = False
        self.__paused = False

    def stop(self) -> None:
        self.__ticks = 0
        self.__loop = self.__loops
        self.__ended = True
        self.__paused = False

    def pause(self) -> None:
        self.__paused = True

    def resume(self) -> None:
        self.__paused = False

    def update(self) -> None:
        if self.__ended or self.__paused:
            return

        self.__ticks += 1

        if self.__ticks >= self.__interval:
            self.__loop -= 1
            self.__ended = self.__loop <= 0
            if not self.__ended:
                self.__ticks = 1
            if self.__on_end_func is not None:
                self.__on_end_func()

        elif self.__on_update_func is not None:
            self.__on_update_func(self.__interval, self.__ticks)
