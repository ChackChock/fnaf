from scripts import gui
from scripts.system import cursors, display

from .. import network

from .base_window import BaseWindow


class ClientRoomWindow(BaseWindow):
    name = "client-room"

    def __connect_to_room(self) -> None:
        try:
            network.start_client(input("--> "))

            self.__layout.clear()
            self.__layout.add(
                [
                    gui.Label(0, "Ожидайте начала игры!", "main"),
                    self.__label,
                ]
            )

        except Exception:
            print("Вы ввели неверный ip!")

    def _build(self):
        self.__label = gui.Label(0, "Подключилось: 0", "main-small")
        self.__layout = gui.VerticalLayout(display.get_surface_center(), 10)

        self.__layout.add(
            [
                gui.Label(0, "Введите ip сервера:", "main"),
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Подключиться", "main"),
                    click_listener=lambda w, e: self.__connect_to_room(),
                ),
            ]
        )

        main_layout = gui.FloatLayout(0)
        main_layout.add([self.__layout])

        return main_layout

    def load(self) -> None:
        super().load()
        display.set_clear_color((255, 255, 255))

    def update(self) -> None:
        super().update()

        data = network.get_data()
        if data:
            amount = 0

            for x in data:
                if x["key"] == "game-started":
                    self._start_window_change("game")
                else:
                    amount = max(amount, x["data"]["members"])

            if amount > 0:
                self.__label.set_text(f"Подключилось: {amount}")
