"""This module provides classes for GUI widgets event handling in a
Pygame-based application.

Classes:
    - WidgetConnectionManager: Class for connecting widget events to an event system
    function.
    - WidgetEventSystem: Class for managing events related to a widget.
    - Widget: Class representing a GUI widget.
"""

__all__ = ["WidgetConnectionManager", "WidgetEventSystem", "Widget"]


from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, final

import pygame

from ..models import events
from ..models.exceptions import WidgetHasParentError
from ..models.gui_enums import Anchors
from ..models.types import Coordinate
from ..system import mouse
from ..utils import gui_functions


type AnyWidget = Any
"""Represents any type of any widget."""
type listener = Callable[[AnyWidget, pygame.Event], Any]
"""Represents a type hint for a listener function that takes arguments of type
any widget and pygame.Event.
"""


class WidgetConnectionManager:
    """Class that connects widget events to a specified event system function.

    Args:
        event_system_func (Callable[[int, listener], None]): A function to handle events.

    Methods:
        - hover(listener: listener) -> None: int 'HOVER' event for the given
        listener.
        - hover_out(listener: listener) -> None: int 'HOVER_OUT' event for the
        given listener.
        - hover_in(listener: listener) -> None: int 'HOVER_IN' event for the
        given listener.
        - scroll_wheel_up(listener: listener) -> None: int 'SCROLL_WHEEL_UP'
        event for the given listener.
        - scroll_wheel_down(listener: listener) -> None: int 'SCROLL_WHEEL_DOWN'
        event for the given listener.
        - drag(listener: listener) -> None: int 'DRAG' event for the given
        listener.
        - hold(listener: listener) -> None: int 'HOLD' event for the given
        listener.
        - release(listener: listener) -> None: int 'RELEASE' event for the given
        listener.
        - press(listener: listener) -> None: int 'PRESS' event for the given
        listener.
    """
    def __init__(self, event_system_func: Callable[[int, listener], None]) -> None:
        self._event_system_func = event_system_func

    def hover(self, listener: listener) -> None:
        """int the 'HOVER' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.HOVER, listener)

    def hover_out(self, listener: listener) -> None:
        """int the 'HOVER_OUT' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.HOVER_OUT, listener)

    def hover_in(self, listener: listener) -> None:
        """int the 'HOVER_IN' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.HOVER_IN, listener)

    def scroll_wheel_up(self, listener: listener) -> None:
        """int the 'SCROLL_WHEEL_UP' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.SCROLL_WHEEL_UP, listener)

    def scroll_wheel_down(self, listener: listener) -> None:
        """int the 'SCROLL_WHEEL_DOWN' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.SCROLL_WHEEL_DOWN, listener)

    def drag(self, listener: listener) -> None:
        """int the 'DRAG' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.DRAG, listener)

    def hold(self, listener: listener) -> None:
        """int the 'HOLD' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.HOLD, listener)

    def release(self, listener: listener) -> None:
        """int the 'RELEASE' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.RELEASE, listener)

    def press(self, listener: listener) -> None:
        """int the 'PRESS' event for the specified listener.

        Args:
            listener (listener): The listener for the event.
        """
        self._event_system_func(events.PRESS, listener)

    def on_prev_update(self, listener: listener) -> None:
        self._event_system_func(events.ON_PREV_UPDATE, listener)

    def on_post_update(self, listener: listener) -> None:
        self._event_system_func(events.ON_POST_UPDATE, listener)

    def on_prev_render(self, listener: listener) -> None:
        self._event_system_func(events.ON_PREV_RENDER, listener)

    def on_post_render(self, listener: listener) -> None:
        self._event_system_func(events.ON_POST_RENDER, listener)


class WidgetEventSystem:
    """A class to manage events related to a widget.

    Args:
        - widget (Widget): The widget associated with the event system.
        - triggers (Optional[Dict[int, List[listener]]]): A dictionary containing
        event triggers and listeners.
        - disabled (bool): Flag to indicate if the event system is disabled. Default is
        False.

    Attributes:
        - _widget (Widget): The widget associated with the event system.
        - _widget_pressed (List[bool]): List to track the pressed state of each widget
        button.
        - _widget_hovered (bool): Flag to indicate if the widget is currently being
        hovered over.

    Properties:
        - hovered (bool): Returns the status of widget_hovered.
        - disabled (bool): Returns the status of the event system's disabled flag.
        - triggers (Dict[int, List[listener]]): Returns a copy of the triggers
        dictionary.

    Methods:
        - _trigger_event(event: pygame.Event) -> None: int the specified event with
        the associated listeners.
        - add_listener(event: int, listener: listener) -> None: Adds a new listener
        for a specific event.
        - remove_listener(event: int, listener: listener) -> None: Removes a listener
        for a specific event.
        - get_pressed(index: int) -> bool: Returns the pressed state of a specific button
        index.
        - set_disabled(value: bool) -> None: Sets the disabled flag of the event system.
        - uptate() -> None: Updates the event system if the widget is not disabled.
        - _on_uptate() -> None: Handles the update logic for event triggers based on
        mouse interactions.
    """
    def __init__(
        self,
        widget: "Widget",
        triggers: Optional[Dict[int, List[listener]]] = None,
        disabled: bool = False,
    ) -> None:
        self.__disabled = disabled
        if triggers is None:
            self.__triggers: Dict[int, List[listener]] = dict()
        else:
            self.__triggers = {key: value.copy() for key, value in triggers.items()}

        self._widget = widget
        self._widget_pressed: List[bool] = [False for _ in range(3)]
        self._widget_hovered = False

    @property
    def widget_hovered(self) -> bool:
        """Get the hovering status of the widget.

        Returns:
            bool: True if the widget is currently being hovered over, False otherwise.
        """
        return self._widget_hovered

    @property
    def disabled(self) -> bool:
        """Get the disabled status of the event system.

        Returns:
            bool: True if the event system is disabled, False otherwise.
        """
        return self.__disabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.__disabled = value

    @property
    def triggers(self) -> Dict[int, List[listener]]:
        """Get triggers dictionary.

        Returns:
            Dict[int, List[listener]]: int dictionary.
        """
        return {key: value.copy() for key, value in self.__triggers.items()}

    def _on_update(self) -> None:
        """Internal method to handle update logic for the event system."""
        if self.__disabled:
            return

        hit = self._widget.collide_point(mouse.get_coords())

        if self._widget_hovered:
            if hit:
                self._trigger_event(
                    pygame.Event(events.HOVER, user_event=True)
                )
            else:
                self._trigger_event(
                    pygame.Event(events.HOVER_OUT, user_event=True)
                )
                self._widget_hovered = False
        elif hit:
            self._trigger_event(
                pygame.Event(events.HOVER_IN, user_event=True)
            )
            self._widget_hovered = True

        if self._widget_hovered:
            if mouse.get_wheel() == mouse.MouseWheelStates.UP:
                self._trigger_event(
                    pygame.Event(events.SCROLL_WHEEL_UP, user_event=True)
                )
            elif mouse.get_wheel() == mouse.MouseWheelStates.DOWN:
                self._trigger_event(
                    pygame.Event(events.SCROLL_WHEEL_DOWN, user_event=True)
                )
            mouse.add_hovered_widgets(self._widget)

        for i in range(1, 4):
            button = mouse.get_button(i)

            if self._widget_pressed[i - 1]:
                if button.state == mouse.MouseButtonStates.HOLD:
                    if mouse.motion():
                        mouse.add_interacted_widgets(self._widget)
                        self._trigger_event(pygame.Event(
                                events.DRAG, button=button, hit=hit, user_event=True
                            )
                        )
                    else:
                        mouse.add_interacted_widgets(self._widget)
                        self._trigger_event(pygame.Event(
                                events.HOLD, button=button, hit=hit, user_event=True
                            )
                        )

                elif button.state == mouse.MouseButtonStates.RELEASE:
                    mouse.add_interacted_widgets(self._widget)
                    self._trigger_event(pygame.Event(
                            events.RELEASE, button=button, hit=hit, user_event=True
                        )
                    )
                    self._widget_pressed[i - 1] = False

            elif hit and button.state == mouse.MouseButtonStates.PRESS:
                mouse.add_interacted_widgets(self._widget)
                self._trigger_event(pygame.Event(
                        events.PRESS, button=button, hit=hit, user_event=True
                    )
                )
                self._widget_pressed[i - 1] = True

    def _trigger_event(self, event: pygame.Event) -> None:
        """Internal method to trigger an event for the specified event type.

        Args:
            event (pygame.Event): The pygame event object.
        """
        if event.type in self.__triggers:
            for listener in self.__triggers[event.type]:
                listener(self._widget, event)

    def add_listener(
        self,
        event: int,
        listener: listener,
    ) -> None:
        """Add a listener function for a specific event type.

        Args:
            event (int): The event type to listen for.
            listener (listener): The listener function to be added.
        """
        if event in self.__triggers:
            self.__triggers[event].append(listener)
        else:
            self.__triggers[event] = [listener]

    def remove_listener(
        self,
        event: int,
        listener: listener,
    ) -> None:
        """Remove a listener function for a specific event type.

        Args:
            event (int): The event type to remove the listener from.
            listener (listener): The listener function to be removed.
        """
        if event in self.__triggers:
            self.__triggers[event].remove(listener)

    def get_pressed(self, index: int) -> bool:
        """Check if a specific button is currently pressed.

        Args:
            index (int): The index of the button to check (1-3).
        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return self._widget_pressed[index - 1]

    @final
    def uptate(self) -> None:
        """Update the event system and trigger events based on widget interactions."""
        if self.__disabled:
            return
        self._on_update()


class Widget:
    """A class representing a GUI widget.

    Args:
        - center (Coordinate): The coordinates of the center of the widget.
        - image (Optional[pygame.Surface]): The image representing the widget.
        Default is None.
        - active (bool): Flag to indicate if the widget is active. Default is True.
        - anchor (Anchors): The anchor point of the widget. Default is Anchors.CENTER.
        - tags (Optional[Sequence[str]]): Tags associated with the widget. Default is
        None.

    Attributes:
        - _event_system (WidgetEventSystem): Event system for handling widget events.
        - _disconnector (WidgetConnectionManager): Connection manager for removing
        event listeners.
        - _connector (WidgetConnectionManager): Connection manager for adding event
        listeners.
        - _image (Optional[pygame.Surface]): The image surface of the widget.
        - _rect (pygame.FRect): The rectangle boundary of the widget.

    Properties:
        - id (int): Returns the unique identifier of the widget.
        - tags (Set[str]): Returns a copy of the tags associated with the widget.
        - connect (WidgetConnectionManager): Returns the connector for adding event
        listeners.
        - disconnect (WidgetConnectionManager): Returns the disconnector for removing
        event listeners.
        - hovered (bool): Returns the hover status of the widget.
        - disabled (bool): Returns the disabled status of the widget.
        - active (bool): Returns the active status of the widget.
        - anchor (Anchors): Returns the anchor point of the widget.
        - parent (Optional["Widget"]): Returns the parent widget of the current widget.

    Methods:
        - _set_image(value: Optional[pygame.Surface], anchor: Anchors = Anchors.CENTER) -> None: Sets the image and rectangle of the widget.
        - _on_update() -> None: Updates the widget's event system if active.
        - _on_render(surface: pygame.Surface, offset: Coordinate) -> None: Renders the
        widget on a surface with an offset.
        - update() -> None: Updates the widget if active.
        - render(surface: pygame.Surface, offset: Coordinate = 0) -> None: Renders the
        widget on a surface with an offset.
        - get_pressed(index: int) -> bool: Returns the pressed state of a specific
        button index.
        - get_relative_rect() -> pygame.FRect: Returns the relative rectangle of the
        widget.
        - get_absolute_rect() -> pygame.FRect: Returns the absolute rectangle of the
        widget.
        - get_size() -> Tuple[float, float]: Returns the size of the widget.
        - get_width() -> float: Returns the width of the widget.
        - get_height() -> float: Returns the height of the widget.
        - collide_point(point: Coordinate) -> bool: Checks if a point collides with the
        widget.
        - set_disabled(value: bool) -> None: Sets the disabled status of the widget.
        - move(x: Coordinate) -> None: Moves the widget by a certain amount.
        - move_to(x: Coordinate, anchor: Optional[Anchors] = None) -> None: Moves the
        widget to a specific position.
        - add_tag(tag: str) -> None: Adds a tag to the widget.
        - add_tags(tags: Sequence[str]) -> None: Adds multiple tags to the widget.
        - remove_tag(tag: str) -> None: Removes a tag from the widget.
        - remove_tags(tags: Sequence[str]) -> None: Removes multiple tags from the
        widget.
    """
    def __init__(
        self,
        center: Coordinate,
        image: Optional[pygame.Surface] = None,
        active: bool = True,
        anchor: Anchors = Anchors.CENTER,
        tags: Optional[Sequence[str]] = None,
    ) -> None:
        self.__id = gui_functions.generate_widget_id()
        self.__tags: Set[str] = set() if tags is None else set(tags)
        self.__active = active
        self.__anchor = anchor
        self.__parent: Optional[AnyWidget] = None

        self._event_system = WidgetEventSystem(self)
        self._disconnector = WidgetConnectionManager(self._event_system.remove_listener)
        self._connector = WidgetConnectionManager(self._event_system.add_listener)

        if image is None:
            self._image = None
            self._rect = pygame.FRect(pygame.Vector2(center), (0, 0))
        else:
            self._image = image.copy()
            self._rect = self._image.get_frect(**{self.__anchor:pygame.Vector2(center)})

        gui_functions.add_widget(self)

    def __repr__(self) -> str:
        if self.__tags:
            return f"<{self.__class__.__name__}: id: {self.__id}, tags: {", ".join(self.__tags)}>"
        return f"<{self.__class__.__name__}: id: {self.__id}>"

    def __del__(self) -> None:
        gui_functions.delete_widget(self)

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__ or key.startswith("__"):
            return self.__dict__[key]
        raise KeyError(f"Object {self} has no attribute `{key}`!")

    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self.__dict__ or key.startswith("__"):
            raise KeyError(f"Object {self} has no attribute `{key}`!")
        self.__dict__[key] = value

    @property
    def id(self) -> int:
        """Get the unique identifier of the widget.

        Returns:
            int: The unique identifier of the widget.
        """
        return self.__id

    @property
    def tags(self) -> Set[str]:
        """Get a copy of the set of tags associated with the widget.

        Returns:
            Set[str]: A copy of the set of tags.
        """
        return self.__tags.copy()

    @property
    def connect(self) -> WidgetConnectionManager:
        """Get a WidgetConnectionManager instance for connecting listeners to events.

        Returns:
            WidgetConnectionManager: A WidgetConnectionManager instance for connecting
            listeners.
        """
        return self._connector

    @property
    def disconnect(self) -> WidgetConnectionManager:
        """Get a WidgetConnectionManager instance for disconnecting listeners from events.

        Returns:
            WidgetConnectionManager: A WidgetConnectionManager instance for disconnecting listeners.
        """
        return self._disconnector

    @property
    def hovered(self) -> bool:
        """Get the hovering status of the widget.

        Returns:
            bool: True if the widget is currently being hovered over, False otherwise.
        """
        return self._event_system.widget_hovered

    @property
    def anchor(self) -> Anchors:
        """Get the anchor point of the widget.

        Args:
            value (Anchors): The new anchor point for the widget.

        Returns:
            Anchors: The anchor point of the widget.
        """
        return self.__anchor

    @anchor.setter
    def anchor(self, value: Anchors) -> None:
        self.__anchor = value

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, value: bool) -> None:
        from .layouts import Container

        self.__active = value
        if value and issubclass(type(self.__parent), Container):
            self.__parent.set_children_position()  # type: ignore

    def _on_update(self) -> None:
        """Update method that calls the event system to update the widget."""
        self._event_system._trigger_event(
            pygame.Event(events.ON_PREV_UPDATE, user_event=True)
        )
        self._event_system.uptate()
        self._event_system._trigger_event(
            pygame.Event(events.ON_POST_UPDATE, user_event=True)
        )

    def _on_render(self, surface: pygame.Surface, offset: Coordinate) -> None:
        """Render the widget on the given surface with the specified offset.

        Args:
            surface (pygame.Surface): The surface to render the widget on.
            offset (Coordinate): The offset for rendering the widget.
        """
        self._event_system._trigger_event(
            pygame.Event(
                events.ON_PREV_RENDER, surface=surface, offset=offset, user_event=True
            )
        )
        if self._image is not None:
            surface.blit(
                self._image, self.get_absolute_rect().move(- pygame.Vector2(offset))
            )
        self._event_system._trigger_event(
            pygame.Event(
                events.ON_POST_RENDER, surface=surface, offset=offset, user_event=True
            )
        )

    @final
    def update(self) -> None:
        """Final method to update the widget if it is active."""
        if self.__active:
            self._on_update()

    @final
    def render(self, surface: pygame.Surface, offset: Coordinate = 0) -> None:
        """Final method to render the widget on the specified surface with an offset.

        Args:
            surface (pygame.Surface): The surface to render the widget on.
            offset (Coordinate, optional): The offset for rendering the widget.
            Defaults to 0.
        """
        if self.__active:
            self._on_render(surface, offset)

    def get_info(self) -> str:
        return "\n".join([
            f"{self.__class__.__name__}:",
            f"  - id: {self.__id}",
            f"  - anchor: {self.__anchor}",
            f"  - tags: {list(self.__tags)}",
            f"  - absolute rect: {tuple(self.get_absolute_rect())}",
            f"  - relative rect: {tuple(self.get_relative_rect())}",
            f"  - parent: {self.__parent}",
        ])

    def get_cursor(self) -> Optional[pygame.Cursor]:
        return None

    def get_image(self) -> Optional[pygame.Surface]:
        return None if self._image is None else self._image.copy()

    def get_pressed(self, index: int) -> bool:
        """Check if a specific button is currently pressed.

        Args:
            index (int): The index of the button to check (1-3).

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return self._event_system.get_pressed(index)

    def get_relative_rect(self) -> pygame.FRect:
        """Get the relative rectangle of the widget.

        Returns:
            pygame.FRect: The relative rectangle of the widget.
        """
        return self._rect.copy()

    def get_absolute_rect(self) -> pygame.FRect:
        """Get the absolute rectangle of the widget.

        Returns:
            pygame.FRect: The absolute rectangle of the widget.
        """
        if self.__parent is None:
            return self.get_relative_rect()
        return self._rect.move(self.__parent.get_absolute_rect().topleft)

    def get_size(self) -> Tuple[float, float]:
        """Get the size of the widget.

        Returns:
            Tuple[float, float]: The width and height of the widget.
        """
        return self._rect.size

    def get_width(self) -> float:
        """Get the width of the widget.

        Returns:
            float: The width of the widget.
        """
        return self._rect.width

    def get_height(self) -> float:
        """Get the height of the widget.

        Returns:
            float: The height of the widget.
        """
        return self._rect.height

    def get_parent(self) -> AnyWidget:
        """Returns the parent of the widget.

        Returns:
            AnyWidget: The parent of the widget.
        """
        return self.__parent

    def set_image(
        self, value: Optional[pygame.Surface], anchor: Anchors = Anchors.CENTER
    ) -> None:
        """Set the image of the widget and update its position based on the anchor.

        Args:
            value (Optional[pygame.Surface]): The image to set for the widget.
            anchor (Anchors, optional): The anchor point for positioning the image.
            Defaults to Anchors.CENTER.
        """
        from .layouts.container import Container

        if value is None:
            self._image = None
            self._rect = pygame.FRect(getattr(self._rect, anchor), (0, 0))
        else:
            self._image = value.copy()
            self._rect = self._image.get_frect(**{anchor: getattr(self._rect, anchor)})
        if issubclass(type(self.__parent), (Container)):
            self.__parent.set_children_position()  # type: ignore

    def set_parent(self, parent: AnyWidget) -> None:
        """Sets the parent for the widget.

        Args:
            parent (AnyWidget): The parent widget to be set.

        Raises:
            WidgetHasParentError: If the widget already has a parent assigned.
        """
        if not (self.__parent is None or parent is None):
            raise WidgetHasParentError(
                f"Widget {self} cannot set the parent {parent}, because it already has {self.__parent} parent!"
            )
        self.__parent = parent

    def collide_point(self, point: Coordinate) -> bool:
        """Check if a point collides with the widget.

        Args:
            point (Coordinate): The coordinate to check for collision.

        Returns:
            bool: True if the point collides with the widget, False otherwise.
        """
        return self.get_absolute_rect().collidepoint(pygame.Vector2(point))

    def set_disabled(self, value: bool) -> None:
        """Set the disabled status of the widget.

        Args:
            value (bool): True to disable the widget, False to enable it.
        """
        self._event_system.disabled = value

    def move(self, x: Coordinate) -> None:
        """Move the widget by a specified distance along the x-axis.

        Args:
            x (Coordinate): The distance to move the widget along the x-axis.
        """
        self._rect.move_ip(pygame.Vector2(x))

    def move_to(self, x: Coordinate, anchor: Optional[Anchors] = None) -> None:
        """Move the widget to a specific position on the x-axis.

        Args:
            x (Coordinate): The x-coordinate to move the widget to.
            anchor (Optional[Anchors]): The anchor point to use for positioning.
        """
        if anchor is None:
            anchor = self.__anchor
        setattr(self._rect, anchor, pygame.Vector2(x))

    def add_tag(self, tag: str) -> None:
        """Add a tag to the widget.

        Args:
            tag (str): The tag to add to the widget.
        """
        self.__tags.add(tag)

    def add_tags(self, tags: Sequence[str]) -> None:
        """Add multiple tags to the widget.

        Args:
            tags (Sequence[str]): The list of tags to add to the widget.
        """
        self.__tags.update(tags)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the widget if it exists.

        Args:
            tag (str): The tag to remove from the widget.
        """
        if tag in self.__tags:
            self.__tags.remove(tag)

    def remove_tags(self, tags: Sequence[str]) -> None:
        """Remove multiple tags from the widget.

        Args:
            tags (Sequence[str]): The list of tags to remove from the widget.
        """
        for tag in tags:
            self.remove_tag(tag)
