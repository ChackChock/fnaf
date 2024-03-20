from dataclasses import dataclass, field
import pickle
import socket
import threading
from typing import Any, List, Optional


@dataclass
class __Info:
    clients: List[socket.socket] = field(default_factory=list)
    data: List[Any] = field(default_factory=list)
    mode: Optional[str] = None


def __handle_client(conn: socket.socket):
    try:
        connected = True
        while connected:
            data = pickle.loads(conn.recv(1024))

            if data:
                __info.data.append(data)
                for client in __info.clients:
                    if client is not conn:
                        client.sendall(pickle.dumps(data))
            else:
                connected = False

    except Exception:
        pass
    finally:
        conn.close()


def __start_server() -> None:
    print("Start server")
    __socket.bind(__addr)
    __socket.listen()

    while True:
        conn, _ = __socket.accept()
        __info.clients.append(conn)
        threading.Thread(target=__handle_client, args=(conn,)).start()


def __start_client():
    print("Start client")
    __socket.connect(__addr)

    try:
        while True:
            data = pickle.loads(__socket.recv(1024))
            __info.data.append(data)
    except Exception:
        pass


def start_client() -> None:
    if __info.mode is not None:
        raise Exception()

    threading.Thread(target=__start_client).start()
    __info.mode = "client"


def start_server() -> None:
    if __info.mode is not None:
        raise Exception()

    threading.Thread(target=__start_server).start()
    __info.mode = "server"


def send_message(data: Any) -> None:
    if __info.mode == "client":
        __socket.send(pickle.dumps(data))

    else:
        for client in __info.clients:
            client.sendall(pickle.dumps(data))


def close() -> None:
    __socket.close()


def get_data() -> List[Any]:
    data = __info.data.copy()
    __info.data.clear()
    return data


def get_mode() -> Optional[str]:
    return __info.mode


__addr = ("localhost", 5050)
__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
__info = __Info()
