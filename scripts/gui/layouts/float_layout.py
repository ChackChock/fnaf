from typing import Optional, Sequence
import pygame

from ...models.gui_enums import Anchors
from ...models.types import Coordinate

from .container import Container


class FloatLayout(Container):
    def __init__(
        self,
        topleft: Coordinate,
        active: bool = True,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(topleft, active, Anchors.TOPLEFT, tags)

    def set_children_position(self) -> None:
        rightbottom = pygame.Vector2(-float("inf"))

        for child in self.get_children(True):
            rect: pygame.FRect = child.get_absolute_rect()
            rightbottom.x = max(rightbottom.x, rect.right)
            rightbottom.y = max(rightbottom.y, rect.bottom)

        self._rect = pygame.FRect(self._rect.topleft, rightbottom - self._rect.topleft)
