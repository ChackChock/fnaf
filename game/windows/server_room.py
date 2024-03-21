import socket

from scripts import gui
from scripts.system import cursors, display

from .. import network

from .base_window import BaseWindow


class ServerRoomWindow(BaseWindow):
    name = "server-room"

    def __connect_to_room(self) -> None:
        network.send_message("game-started", None)
        self._start_window_change("game")

    def _build(self):
        main_layout = gui.FloatLayout(0)
        self.__label = gui.Label(0, "Подключилось: 1", "main-small")

        layout = gui.VerticalLayout(display.get_surface_center(), 10)
        layout.add(
            [
                gui.Label(
                    0, f"Ваш ip: {socket.gethostbyname(socket.gethostname())}", "main"
                ),
                self.__label,
                gui.Button(
                    0,
                    hovered_cursor=cursors.get_cursor("pointer-1"),
                    clicked_cursor=cursors.get_cursor("pointer-2"),
                    label=gui.Label(0, "Начать игру", "main"),
                    click_listener=lambda w, e: self.__connect_to_room(),
                ),
            ]
        )

        main_layout.add([layout])

        return main_layout

    def load(self) -> None:
        super().load()
        network.start_server()
        display.set_clear_color((255, 255, 255))

    def update(self) -> None:
        super().update()

        data = network.get_data()
        if data:
            amount = max([x["data"]["members"] for x in data])
            self.__label.set_text(f"Подключилось: {amount}")
