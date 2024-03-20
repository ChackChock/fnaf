"""Module providing functions to manage widgets within a widget collection.

This module defines functions to generate, add, delete, and retrieve widgets
based on various criteria such as ID, tags, and classes.

Functions:
    - get_widget_by_id(id: int) -> Optional[AnyWidget]: Retrieve a widget by its ID.
    - get_widgets_by_tags(*tags: str) -> List[AnyWidget]: Retrieve widgets by specified tags.
    - get_widgets_by_classes(*classes: Type[AnyWidget]) -> List[AnyWidget]: Retrieve widgets by specified classes.

Notes:
    - Advised not to use functions `generate_widget_id`, `add_widget` and
    `delete_widget` because they are necessary for the correct operation of the module
    and are called in the Widget class (module scripts/gui/widget.py)
"""

__all__ = ["get_widget_by_id", "get_widgets_by_tags", "get_widgets_by_classes"]


from typing import TYPE_CHECKING, Dict, List, Optional, Type

if TYPE_CHECKING:
    from ..gui.widget import AnyWidget


def generate_widget_id() -> int:
    """Generate a new unique widget ID based on the total number of existing widgets.

    Returns:
        int: A new unique widget ID.
    """
    return len(__widgets)


def add_widget(widget: "AnyWidget") -> None:
    """Add a new widget to the widget collection.

    Args:
        widget (Widget): The widget object to add to the collection.
    """
    __widgets[widget.id] = widget


def delete_widget(widget: "AnyWidget") -> None:
    """Delete a widget from the widget collection.

    Args:
        widget (Widget): The widget object to delete from the collection.
    """
    __widgets.pop(widget.id)


def get_widget_by_id(id: int) -> Optional["AnyWidget"]:
    """Retrieve a widget from the collection based on the provided ID.

    Args:
        id (int): The ID of the widget to retrieve.

    Returns:
        Optional[AnyWidget]: The widget object if found, None otherwise.
    """
    return __widgets.get(id, None)


def get_widgets_by_tags(*tags: str) -> List["AnyWidget"]:
    """Return a list of widgets that have all the specified tags.

    Args:
        *tags (str): Variable number of tag strings to filter widgets.

    Returns:
        List[AnyWidget]: A list of widgets that have all the specified tags.
    """
    values = set(tags)
    return [widget for widget in __widgets.values() if widget.tags >= values]


def get_widgets_by_classes(*classes: Type["AnyWidget"]) -> List["AnyWidget"]:
    """Return a list of widgets that belong to one or more of the specified classes.

    Args:
        *classes (Type[AnyWidget]): Variable number of Widget classes to filter widgets.

    Returns:
        List[AnyWidget]: A list of widgets that belong to the specified classes.
    """
    return [
        widget for widget in __widgets.values() if issubclass(type(widget), classes)
    ]


__widgets: Dict[int, "AnyWidget"] = dict()
