""""""

__all__ = ["Container"]


from typing import List, Optional, Sequence, SupportsIndex, Union, overload

import pygame

from ..widget import Widget, AnyWidget

from ...models.gui_enums import Anchors
from ...models.types import Coordinate


class Container(Widget):
    def __init__(
        self,
        center: Coordinate,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(center, None, active, anchor, tags=tags)

        self.__children: List[AnyWidget] = list()

    def _add(self, child: AnyWidget) -> None:
        if not issubclass(type(child), Widget):
            raise ValueError()
        child.set_parent(self)
        self.__children.append(child)
        self.set_children_position()

    def _remove(self, child: AnyWidget) -> None:
        child.set_parent(None)
        self.__children.remove(child)
        self.set_children_position()

    def _on_update(self) -> None:
        for child in reversed(self.__children):
            child.update()
        super()._on_update()

    def _on_render(self, surface: pygame.Surface, offset: Coordinate) -> None:
        super()._on_render(surface, offset)
        for child in self.__children:
            child.render(surface, offset)

    def get_info(self) -> str:
        return "\n".join([
            f"{self.__class__.__name__}:",
            f"  - id: {self.id}",
            f"  - children amount: {len(self.__children)}",
            f"  - anchor: {self.anchor}",
            f"  - tags: {list(self.tags)}",
            f"  - absolute rect: {tuple(self.get_absolute_rect())}",
            f"  - relative rect: {tuple(self.get_relative_rect())}",
            f"  - parent: {self.get_parent()}",
        ])

    def get_children(self, only_active: bool = False) -> List[AnyWidget]:
        if only_active:
            return list(filter(lambda w: w.active, self.__children))

        return self.__children.copy()

    @overload
    def add(self, x: AnyWidget) -> None: ...
    @overload
    def add(self, x: Sequence[AnyWidget]) -> None: ...
    def add(self, x: Union[AnyWidget, Sequence[AnyWidget]]) -> None:
        if isinstance(x, Sequence):
            for widget in x:
                self._add(widget)
        else:
            self._add(x)

    @overload
    def remove(self, x: AnyWidget) -> None: ...
    @overload
    def remove(self, x: Sequence[AnyWidget]) -> None: ...
    def remove(self, x: Union[AnyWidget, Sequence[AnyWidget]]) -> None:
        if isinstance(x, Sequence):
            for widget in x:
                self._remove(widget)
        else:
            self._remove(x)

    def insert_widget(self, index: SupportsIndex, widget: AnyWidget) -> None:
        parent = widget.get_parent()
        if parent is not None and issubclass(type(parent), Container):
            parent.remove(widget)

        widget.set_parent(self)
        self.__children.insert(index, widget)
        self.set_children_position()

    def insert_widgets(
        self, index: SupportsIndex, widgets: Sequence[AnyWidget]
    ) -> None:
        for i, widget in enumerate(widgets):
            self.insert_widget(int(index) + i, widget)

    def get_child_index(self, child: AnyWidget) -> int:
        return self.__children.index(child)

    def clear(self) -> None:
        for child in self.__children:
            child.set_parent(None)
            self.__children.remove(child)

    def set_children_position(self) -> None:
        parent = self.get_parent()
        if issubclass(type(parent), Container):
            parent.set_children_position()
