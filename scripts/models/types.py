from typing import Protocol, SupportsIndex, Union

import pygame


class Sequence[_T](Protocol):
    """An abstract base class representing a sequence of elements."""
    def __getitem__(self, __i: SupportsIndex) -> _T: ...
    def __len__(self) -> int: ...


type ColorValue = Union[int, str, Sequence[int]]
"""A type representing a color value that can be an integer, string,
or a sequence of integers.
"""
type Coordinate = Union[str, float, Sequence[float], pygame.Vector2]
"""CoordinateType is a union type that can be either a string, a float, a sequence of
floats, or a pygame.Vector2.
"""
