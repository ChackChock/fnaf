__all__ = ["ButtonConnectionManager", "ButtonEventSystem", "Button", "AnimatedButton"]


from typing import Any, Optional, Sequence

import pygame

from .widget import Widget, WidgetConnectionManager, WidgetEventSystem, listener
from .label import Label

from ..models import events
from ..models.gui_enums import Anchors
from ..models.types import Coordinate


class ButtonConnectionManager(WidgetConnectionManager):
    def click(self, listener: listener) -> None:
        self._event_system_func(events.CLICK, listener)


class ButtonEventSystem(WidgetEventSystem):
    def _trigger_event(self, event: pygame.Event) -> None:
        if (
            event.type == events.RELEASE
            and self.get_pressed(event.button.num)
            and event.hit
        ):
            self._trigger_event(pygame.Event(events.CLICK, **event.dict))
        super()._trigger_event(event)


class Button(Widget):
    def __init__(
        self,
        center: Coordinate,
        image: Optional[pygame.Surface] = None,
        *,
        hovered_cursor: pygame.Cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND),
        clicked_cursor: pygame.Cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND),
        label: Optional[Label] = None,
        click_listener: Optional[listener] = None,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(center, image, active, anchor, tags)

        self.__label: Optional[Label] = None
        self.__hovered_cursor = hovered_cursor
        self.__clicked_cursor = clicked_cursor
        self._event_system = ButtonEventSystem(self)
        self._connector = ButtonConnectionManager(self._event_system.add_listener)
        self._disconnector = ButtonConnectionManager(self._event_system.remove_listener)

        if click_listener is not None:
            self._connector.click(click_listener)
        self.set_label(label)

    @property
    def connect(self) -> ButtonConnectionManager:
        return self._connector

    @property
    def disconnect(self) -> ButtonConnectionManager:
        return self._disconnector

    def set_image(
        self, value: Optional[pygame.Surface], anchor: Anchors = Anchors.CENTER
    ) -> None:
        size = self._rect.size
        super().set_image(value, anchor)
        if self.__label is not None:
            self.__label.move(
                (
                    (self._rect.width - size[0]) / 2,
                    (self._rect.height - size[1]) / 2,
                )
            )

    def _on_update(self) -> None:
        if self.__label is not None:
            self.__label.update()
        super()._on_update()

    def _on_render(self, surface: pygame.Surface, offset: Coordinate) -> None:
        super()._on_render(surface, offset)
        if self.__label is not None:
            self.__label.render(surface, offset)

    def get_info(self) -> str:
        return "\n".join([
            f"{self.__class__.__name__}:",
            f"  - id: {self.id}",
            f"  - label: {self.__label}",
            f"  - anchor: {self.anchor}",
            f"  - tags: {list(self.tags)}",
            f"  - absolute rect: {tuple(self.get_absolute_rect())}",
            f"  - relative rect: {tuple(self.get_relative_rect())}",
            f"  - parent: {self.get_parent()}",
        ])

    def get_cursor(self) -> Optional[pygame.Cursor]:
        if any(self.get_pressed(i) for i in range(1, 4)):
            return self.__clicked_cursor
        if self.hovered:
            return self.__hovered_cursor

    def set_label(self, label: Optional[Label], offset: Coordinate = 0) -> None:
        if self._image is None:
            coords = getattr(self._rect, self.anchor)
            if label is None:
                self._rect = pygame.FRect(pygame.Vector2(coords), (0, 0))
            else:
                self._rect = label.get_absolute_rect()
                setattr(self._rect, self.anchor, coords)

        if self.__label is not None:
            self.__label.set_parent(None)
        self.__label = label
        if self.__label is None:
            return

        self.__label.set_parent(self)
        self.__label.move_to(
            (
                (self._rect.width - self.__label.get_width()) / 2,
                (self._rect.height - self.__label.get_height()) / 2,
            ),
            Anchors.TOPLEFT,
        )
        self.__label.move(offset)

    def get_label(self) -> Optional[Label]:
        return self.__label

    def update_label(self, **kwargs: Any) -> None:
        if self.__label is None:
            raise AttributeError(f"Button {self} has no Label!")
        for key, value in kwargs.items():
            self.__label[key] = value


class AnimatedButton(Button):
    def __init__(
        self,
        center: Coordinate,
        released_image: pygame.Surface,
        pressed_image: pygame.Surface,
        *,
        hovered_cursor: pygame.Cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND),
        clicked_cursor: pygame.Cursor = pygame.Cursor(pygame.SYSTEM_CURSOR_HAND),
        label: Optional[Label] = None,
        click_listener: Optional[listener] = None,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(
            center,
            released_image,
            hovered_cursor=hovered_cursor,
            clicked_cursor=clicked_cursor,
            label=label,
            click_listener=click_listener,
            active=active,
            anchor=anchor,
            tags=tags,
        )

        self.__released_image = released_image.copy()
        self.__pressed_image = pressed_image.copy()

        self.connect.press(lambda w, e: self.set_image(self.__pressed_image))
        self.connect.release(lambda w, e: self.set_image(self.__released_image))
