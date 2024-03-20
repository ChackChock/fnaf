class DisplayInitializedError(Exception):
    """Initialize the DisplayInitializedError with the given error message."""


class AudioFormatError(Exception):
    """Exception raised when there is an error related to audio format."""


class NoWindowError(Exception):
    """Exception raised when there are no inheritors of the Window class
    ( scripts/windows/window.py ).
    """


class WindowNotFoundError(Exception):
    """Exception raised when the window was not found."""


class WindowAlreadyExistsError(Exception):
    """Exception raised when the window was not found."""


class WidgetHasParentError(Exception):
    """Exception raised when the window was not found."""
