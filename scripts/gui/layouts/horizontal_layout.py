from typing import Optional, Sequence

import pygame

from .container import Container

from ...models.gui_enums import Anchors, JustifyContent
from ...models.types import Coordinate


class HorizontalLayout(Container):
    def __init__(
        self,
        center: Coordinate,
        padding: float = 0,
        justify_content: JustifyContent = JustifyContent.PADDING,
        length: Optional[float] = None,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(center, active, anchor, tags)

        if justify_content != JustifyContent.PADDING and length is None:
            raise ValueError()

        self.__padding = padding
        self.__justify_content = justify_content
        self.__length = length if length else 0

    @property
    def padding(self) -> float:
        return self.__padding

    @padding.setter
    def padding(self, value: float) -> None:
        self.__padding = value
        self.set_children_position

    def get_info(self) -> str:
        return "\n".join([
            f"{self.__class__.__name__}:",
            f"  - id: {self.id}",
            f"  - children amount: {len(self.get_children())}",
            f"  - padding: {self.__padding}",
            f"  - justify_content: {self.__justify_content}",
            f"  - length: {self.__length}",
            f"  - anchor: {self.anchor}",
            f"  - tags: {list(self.tags)}",
            f"  - absolute rect: {tuple(self.get_absolute_rect())}",
            f"  - relative rect: {tuple(self.get_relative_rect())}",
            f"  - parent: {self.get_parent()}",
        ])

    def set_children_position(self) -> None:
        content_size = pygame.Vector2(-self.__padding, 0)
        children = self.get_children(True)

        for child in children:
            content_size.x += child.get_width()
            content_size.y = max(child.get_height(), content_size.y)

            if self.__justify_content == JustifyContent.PADDING:
                content_size.x += self.__padding

        coords = getattr(self._rect, self.anchor)

        if self.__justify_content == JustifyContent.PADDING:
            self._rect = pygame.FRect((0, 0), content_size)
            padding = self.__padding

        else:
            self._rect = pygame.FRect((0, 0), (self.__length, content_size.y))
            amount = len(children)
            if self.__justify_content == JustifyContent.SPACE_BETWEEN:
                if amount > 1:
                    padding = (self.__length - content_size.x) / (len(children) - 1)
                else:
                    padding = 0
            else:
                padding = (self.__length - content_size.x) / (len(children) + 1)

        setattr(self._rect, self.anchor, coords)

        if self.__justify_content == JustifyContent.SPACE_EVENLY:
            midleft = pygame.Vector2(padding, self._rect.height / 2)
        else:
            midleft = pygame.Vector2(0, self._rect.height / 2)

        for child in self.get_children(True):
            child.move_to(midleft, Anchors.LEFT)
            midleft += (child.get_width() + padding, 0)

        super().set_children_position()
