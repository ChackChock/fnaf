"""This module defines two enumeration classes, Triggers and Anchors, for use in a GUI
application.

Classes:
    - Triggers: Enumeration class to represent different triggering events in a GUI
    application.
    - Anchors: Enumeration class to represent different anchor positions in a GUI
    layout.
"""

__all__ = ["Anchors", "JustifyContent"]


from enum import IntEnum, StrEnum


class Anchors(StrEnum):
    """Enumeration class to represent different anchor positions in a GUI layout."""

    TOPLEFT = "topleft"
    """Anchor position at the top left corner."""

    TOPRIGHT = "topright"
    """Anchor position at the top right corner."""

    BOTTOMLEFT = "bottomleft"
    """Anchor position at the bottom left corner."""

    BOTTOMRIGHT = "bottomright"
    """Anchor position at the bottom right corner."""

    BOTTOM = "midbottom"
    """Anchor position in the middle of the bottom edge."""

    TOP = "midtop"
    """Anchor position in the middle of the top edge."""

    LEFT = "midleft"
    """Anchor position in the middle of the left edge."""

    RIGHT = "midright"
    """Anchor position in the middle of the right edge."""

    CENTER = "center"
    """Anchor position at the center of the layout."""


class JustifyContent(IntEnum):
    PADDING = 0
    SPACE_BETWEEN = 1
    SPACE_EVENLY = 2
