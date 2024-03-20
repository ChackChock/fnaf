from typing import Optional, Sequence

import pygame

from .widget import Widget

from ..models.gui_enums import Anchors
from ..models.types import ColorValue, Coordinate
from ..system import font


class Label(Widget):
    def __init__(
        self,
        center: Coordinate,
        text: str = "",
        font_key: str = "system",
        antialias: bool = True,
        color: ColorValue = (1, 1, 1),
        bgcolor: Optional[ColorValue] = None,
        wraplength: int = 0,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        self.__text = text
        self.__font_key = font_key
        self.__antialias = antialias
        self.__color = color
        self.__bgcolor = bgcolor
        self.__wraplength = wraplength

        super().__init__(
            center,
            self.__convert_text_to_image(),
            active,
            anchor,
            tags,
        )

    def __convert_text_to_image(self) -> pygame.Surface:
        return font.render(
            self.__font_key,
            self.__text,
            self.__antialias,
            self.__color,
            self.__bgcolor,
            self.__wraplength,
        )

    def get_info(self) -> str:
        return "\n".join([
            f"{self.__class__.__name__}:",
            f"  - id: {self.id}",
            f"  - text: {self.__text}",
            f"  - font_key: {self.__font_key}",
            f"  - antialias: {self.__antialias}",
            f"  - color: {self.__color}",
            f"  - bgcolor: {self.__bgcolor}",
            f"  - wraplength: {self.__wraplength}",
            f"  - anchor: {self.anchor}",
            f"  - tags: {list(self.tags)}",
            f"  - absolute rect: {tuple(self.get_absolute_rect())}",
            f"  - relative rect: {tuple(self.get_relative_rect())}",
            f"  - parent: {self.get_parent()}",
        ])

    def get_text(self) -> str:
        return self.__text

    def set_text(
        self,
        text: str = "",
        *,
        font_key: Optional[str] = None,
        antialias: Optional[bool] = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        wraplength: Optional[int] = None,
    ) -> None:
        self.__text = text
        self.__font_key = self.__font_key if font_key is None else font_key
        self.__antialias = self.__antialias if antialias is None else antialias
        self.__color = self.__color if color is None else color
        self.__bgcolor = self.__bgcolor if bgcolor is None else bgcolor
        self.__wraplength = self.__wraplength if wraplength is None else wraplength
        self.set_image(self.__convert_text_to_image())
