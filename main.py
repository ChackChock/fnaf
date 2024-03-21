import pygame


def initialize() -> None:
    from scripts.system import cursors, font, mouse

    font.load("main", 32, "assets", "fonts", "main.ttf")
    font.load("main-small", 22, "assets", "fonts", "main.ttf")

    dir_path = ("assets", "images", "cursors")
    cursors.load_cursor(
        *dir_path, "default.png", key="default", hotspot=(4, 4), size=(32, 32)
    )
    cursors.load_cursor(
        *dir_path, "pointer.png", key="pointer-1", hotspot=(16, 8), size=(32, 32)
    )
    cursors.load_cursor(
        *dir_path, "pointer-click.png", key="pointer-2", hotspot=(16, 8), size=(32, 32)
    )

    mouse.set_default_cursor(cursors.get_cursor("default"))


def create_windows() -> None:
    from game.windows.menu import MenuWindow
    from game.windows.client_room import ClientRoomWindow
    from game.windows.server_room import ServerRoomWindow
    from game.windows.game import GameWindow
    from scripts.windows import manager

    manager.create_window(MenuWindow)
    manager.create_window(ClientRoomWindow)
    manager.create_window(ServerRoomWindow)
    manager.create_window(GameWindow)


def run() -> None:
    from scripts.system.app import App
    from game import network

    app = App(pygame.RESIZABLE | pygame.SCALED, "Pazzles")
    initialize()
    create_windows()

    app.run()
    network.close()


def main() -> None:
    pygame.init()
    run()
    pygame.quit()


if __name__ == "__main__":
    main()
