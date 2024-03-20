"""Module for managing audio files and playback using Pygame library.

Functions
    - load_sound(*paths: str) -> None: Load a sound file into memory for playback.
    - load_sounds(*paths: str) -> None: Load multiple sound files into memory for
    playback.
    - play_sound(sound_name: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) ->
    pygame.mixer.ChannelType: Play a loaded sound by name.
    - stop_sound(sound_name: str) -> None: Stop playing a specific sound.
    - get_sound_volume(sound_name: str) -> float: Get the current volume level of a
    specific sound.
    - set_sound_volume(sound_name: str, volume: float) -> None: Set the volume level of
    a specific sound.
    - set_all_sounds_volume(volume: float) -> None: Set the volume level for all loaded
    sounds.
    - play_music(*paths: str, loops: int = 0, start: float = 0, fade_ms: int = 0) -> None:
    Play music loaded from the specified path.
    - stop_music() -> None: Stop playing the music.
    - get_music_volume() -> float: Get the current volume level of the music.
    - set_music_volume(volume: float) -> None: Set the volume level of the music.
"""

__all__ = [
    "load_sound",
    "load_sounds",
    "play_sound",
    "stop_sound",
    "get_sound_volume",
    "set_sound_volume",
    "set_all_sounds_volume",
    "play_music",
    "stop_music",
    "get_music_volume",
    "set_music_volume",
]


from dataclasses import dataclass, field
from typing import Dict, Tuple
import pygame
import os

from ..models.exceptions import AudioFormatError
from ..utils.file_functions import get_path


@dataclass
class __Data:
    formats: Tuple[str, ...] = (".mp3", ".ogg", ".wav")
    sounds: Dict[str, pygame.mixer.Sound] = field(default_factory=dict)


def load_sound(*paths: str) -> None:
    """Load a sound file into memory for playback.

    Args:
        *paths (str): Variable number of file paths to load.

    Raises:
        AudioFormatError: If the audio format is not suitable.
    """
    path = get_path(*paths)
    if os.path.splitext(path)[1] not in __data.formats:
        raise AudioFormatError(
            f"The audio format `{path}` is not suitable! Suitable formats: {', '.join(__data.formats)}."
        )

    sound_name = os.path.splitext(os.path.basename(path))[0]
    if sound_name not in __data.sounds:
        __data.sounds[sound_name] = pygame.mixer.Sound(path)


def load_sounds(*paths: str) -> None:
    """Load multiple sound files into memory for playback.

    Args:
        *paths (str): Variable number of directories containing sound files.
    """
    path = get_path(*paths)
    for file_name in os.listdir(path):
        load_sound(os.path.join(path, file_name))


def play_sound(
    sound_name: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0
) -> pygame.mixer.ChannelType:
    """Play a loaded sound by name.

    Args:
        sound_name (str): Name of the sound to play.
        loops (int): Number of times to play the sound.
        maxtime (int): Maximum time in milliseconds to play the sound.
        fade_ms (int): Fade in/out time for the sound.

    Returns:
        pygame.mixer.ChannelType: Channel object for the played sound.

    Raises:
        ValueError: If the specified sound name is not uploaded.
    """
    if sound_name in __data.sounds:
        return __data.sounds[sound_name].play(loops, maxtime, fade_ms)
    raise ValueError(
        f"Audio name `{sound_name}` has not been uploaded! Uploaded audio: {', '.join(__data.sounds.keys())}"
    )


def stop_sound(sound_name: str) -> None:
    """Stop playing a specific sound.

    Args:
        sound_name (str): Name of the sound to stop.

    Raises:
        ValueError: If the specified sound name is not uploaded.
    """
    if sound_name in __data.sounds:
        return __data.sounds[sound_name].stop()
    raise ValueError(
        f"Audio name `{sound_name}` has not been uploaded! Uploaded audio: {', '.join(__data.sounds.keys())}"
    )


def get_sound_volume(sound_name: str) -> float:
    """Get the current volume level of a specific sound.

    Args:
        sound_name (str): Name of the sound to get the volume level for.

    Returns:
        float: Current volume level of the specified sound.

    Raises:
        ValueError: If the specified sound name is not uploaded.
    """
    if sound_name in __data.sounds:
        return __data.sounds[sound_name].get_volume()
    raise ValueError(
        f"Audio name `{sound_name}` has not been uploaded! Uploaded audio: {', '.join(__data.sounds.keys())}"
    )


def set_sound_volume(sound_name: str, volume: float) -> None:
    """Set the volume level of a specific sound.

    Args:
        sound_name (str): Name of the sound to set the volume level for.
        volume (float): Volume level to set (0.0 to 1.0).

    Raises:
        ValueError: If the specified sound name is not uploaded.
    """
    if sound_name in __data.sounds:
        return __data.sounds[sound_name].set_volume(volume)
    raise ValueError(
        f"Audio name `{sound_name}` has not been uploaded! Uploaded audio: {', '.join(__data.sounds.keys())}"
    )


def set_all_sounds_volume(volume: float) -> None:
    """Set the volume level for all loaded sounds.

    Args:
        volume (float): Volume level to set for all sounds.
    """
    for sound_name in __data.sounds:
        __data.sounds[sound_name].set_volume(volume)


def play_music(*paths: str, loops: int = 0, start: float = 0, fade_ms: int = 0) -> None:
    """Play music loaded from the specified path.

    Args:
        *paths (str): Variable number of file paths for the music.
        loops (int): Number of times to play the music.
        start (float): Start position in seconds.
        fade_ms (int): Fade in/out time for the music.

    Raises:
        AudioFormatError: If the music format is not suitable.
    """
    path = get_path(*paths)
    if os.path.splitext(path)[1] not in __data.formats:
        raise AudioFormatError(
            f"The audio format is not suitable! Suitable formats: {', '.join(__data.formats)}. The path was passed: {path}"
        )

    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops, start, fade_ms)


def stop_music() -> None:
    """Stop playing the music."""
    pygame.mixer.music.stop()


def get_music_volume() -> float:
    """Get the current volume level of the music.

    Returns:
        float: Current volume level of the music.
    """
    return pygame.mixer.music.get_volume()


def set_music_volume(volume: float) -> None:
    """Set the volume level of the music.

    Args:
        volume (float): Volume level to set (0.0 to 1.0).
    """
    pygame.mixer.music.set_volume(volume)


__data = __Data()
