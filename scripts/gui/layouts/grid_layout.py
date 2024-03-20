import math
from typing import Optional, Sequence

import pygame

from .container import Container

from ...models.gui_enums import Anchors
from ...models.types import Coordinate


class GridLayout(Container):
    def __init__(
        self,
        center: Coordinate,
        length: int,
        padding: float = 0,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(center, active, anchor, tags)

        self.__length = length
        self.__padding = padding

    @property
    def padding(self) -> float:
        return self.__padding

    @padding.setter
    def padding(self, value: float) -> None:
        self.__padding = value
        self.set_children_position()

    def get_length(self) -> int:
        return self.__length

    def set_length(self, value: int) -> None:
        self.__length = value
        self.set_children_position()

    def set_children_position(self) -> None:
        children = self.get_children(True)
        content_size = pygame.Vector2()
        row_content_size = pygame.Vector2()

        for index, child in enumerate(children):
            row_content_size.x += child.get_width() + self.__padding
            row_content_size.y = max(child.get_height(), row_content_size.y)

            if (index + 1) % self.__length == 0:
                content_size.x = max(row_content_size.x, content_size.x)
                content_size.y += row_content_size.y + self.__padding
                row_content_size.update()
        content_size -= (self.__padding, self.__padding)

        coords = getattr(self._rect, self.anchor)
        self._rect = pygame.FRect((0, 0), content_size)
        setattr(self._rect, self.anchor, coords)

        step = pygame.Vector2(
            (content_size.x + self.__padding) / self.__length,
            (content_size.y + self.__padding)
            / math.ceil((len(children) / self.__length)),
        )
        center = pygame.Vector2()
        for index, child in enumerate(children):
            child.move_to(center, anchor=Anchors.TOPLEFT)
            if (index + 1) % self.__length == 0:
                center.update(0, center.y + step.y)
            else:
                center.x += step.x

        super().set_children_position()
