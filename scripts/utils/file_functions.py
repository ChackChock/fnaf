import json
import os
import sys
from typing import Any, Union


__base_path = getattr(
    sys,
    "_MEIPASS",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)


def get_path(*paths: str) -> str:
    """Get the full path by joining the provided paths.

    Args:
        *paths (str): List of strings representing paths to be joined.

    Returns:
        str: Full path after joining.
    """
    return os.path.join(__base_path, *paths)


def read_file(*paths: str, raise_exc: bool = True) -> Union[Any, Exception]:
    """Read and load data from a file.

    Args:
        *paths (str): List of strings representing paths to the file.
        raise_exc (bool, optional): Flag to raise exceptions or return them.
        Defaults to True.

    Returns:
        Union[Any, Exception]: Loaded data if successful, Exception if raise_exc is
        False and an exception is encountered.
    """
    path = get_path(*paths)

    if not os.path.exists(path):
        if raise_exc:
            raise FileNotFoundError(f"File {path} does not exists!")
        else:
            return FileNotFoundError(f"File {path} does not exists!")
    if not os.path.isfile(path):
        if raise_exc:
            raise FileExistsError(f"File {path} does not exists!")
        else:
            return FileExistsError(f"File {path} does not exists!")

    try:
        with open(path, "r") as file:
            data = json.load(file)
    except Exception as exc:
        if raise_exc:
            raise exc
        else:
            return exc

    return data
