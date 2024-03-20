__all__ = [
    "HOVER_IN",
    "HOVER",
    "HOVER_OUT",
    "PRESS",
    "HOLD",
    "DRAG",
    "RELEASE",
    "SCROLL_WHEEL_UP",
    "SCROLL_WHEEL_DOWN",
    "CLICK",
    "SCROLL_SLIDER_UP",
    "SCROLL_SLIDER_DOWN",
    "TOGGLE_ON",
    "TOGGLE_OFF",
]


import pygame


HOVER_IN = pygame.USEREVENT
"""Triggered when the mouse hovers over an widget."""
HOVER = pygame.USEREVENT + 1
"""Triggered when the mouse is hovering over an widget."""
HOVER_OUT = pygame.USEREVENT + 2
"""Triggered when the mouse stops hovering over an widget."""
PRESS = pygame.USEREVENT + 3
"""Triggered when a mouse button is pressed."""
HOLD = pygame.USEREVENT + 4
"""Triggered when a mouse button is being held down."""
DRAG = pygame.USEREVENT + 5
"""Triggered when an widget is being dragged."""
RELEASE = pygame.USEREVENT + 6
"""Triggered when a mouse button is released."""
SCROLL_WHEEL_UP = pygame.USEREVENT + 7
"""Triggered when the mouse wheel is scrolled up."""
SCROLL_WHEEL_DOWN = pygame.USEREVENT + 8
"""Triggered when the mouse wheel is scrolled down."""
CLICK = pygame.USEREVENT + 9
"""Triggered when a mouse button is clicked."""
SCROLL_SLIDER_UP = pygame.USEREVENT + 10
"""Triggered when a scroll slider is moved up."""
SCROLL_SLIDER_DOWN = pygame.USEREVENT + 11
"""Triggered when a scroll slider is moved down."""
TOGGLE_ON = pygame.USEREVENT + 12
"""Triggered when a toggle switch is turned on."""
TOGGLE_OFF = pygame.USEREVENT + 13
"""Triggered when a toggle switch is turned off."""
ON_PREV_UPDATE = pygame.USEREVENT + 14
ON_POST_UPDATE = pygame.USEREVENT + 15
ON_PREV_RENDER = pygame.USEREVENT + 16
ON_POST_RENDER = pygame.USEREVENT + 17


CHANGE_WINDOW = pygame.USEREVENT + 20
