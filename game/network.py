from dataclasses import dataclass, field
import pickle
import socket
import threading
from typing import Any, List, Optional


@dataclass
class __Info:
    connections: List[socket.socket] = field(default_factory=list)
    data: List[Any] = field(default_factory=list)
    mode: Optional[str] = None


def __handle_client(conn: socket.socket) -> None:
    connected = True
    data = {"members": len(__info.connections) + 1}

    send_message("new-client", data)
    __info.data.append({"key": "new-client", "data": data})

    try:
        while connected:
            data = pickle.loads(conn.recv(1024))

            if data:
                __info.data.append(data)
                for connection in __info.connections:
                    if connection is not conn:
                        connection.sendall(pickle.dumps(data))
            else:
                connected = False

    except Exception:
        pass
    finally:
        conn.close()


def __start_server() -> None:
    __socket.bind(("", __port))
    __socket.listen()

    try:
        while True:
            conn, _ = __socket.accept()
            __info.connections.append(conn)
            threading.Thread(target=__handle_client, args=(conn,)).start()
    except Exception:
        pass


def __start_client(ip: str) -> None:
    try:
        while True:
            data = pickle.loads(__socket.recv(1024))
            __info.data.append(data)
    except Exception:
        pass


def start_client(ip: str) -> None:
    if __info.mode is not None:
        raise Exception()

    __socket.connect((ip, __port))
    threading.Thread(target=__start_client, args=(ip,)).start()
    __info.mode = "client"


def start_server() -> None:
    if __info.mode is not None:
        raise Exception()

    threading.Thread(target=__start_server).start()
    __info.mode = "server"


def send_message(key: str, data: Any) -> None:
    if __info.mode == "client":
        __socket.send(pickle.dumps({"key": key, "data": data}))

    else:
        for client in __info.connections:
            client.sendall(pickle.dumps({"key": key, "data": data}))


def close() -> None:
    __socket.close()


def get_data() -> List[Any]:
    data = __info.data.copy()
    __info.data.clear()
    return data


def get_mode() -> Optional[str]:
    return __info.mode


def get_connections() -> List[socket.socket]:
    return __info.connections.copy()


__port = 5050
__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
__info = __Info()
