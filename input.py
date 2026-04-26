from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

import pygame


class Button(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    A = auto()
    B = auto()


@dataclass(frozen=True)
class InputEvent:
    button: Button


KEYBOARD_MAP = {
    pygame.K_UP: Button.UP,
    pygame.K_DOWN: Button.DOWN,
    pygame.K_LEFT: Button.LEFT,
    pygame.K_RIGHT: Button.RIGHT,
    pygame.K_RETURN: Button.A,
    pygame.K_z: Button.A,
    pygame.K_ESCAPE: Button.B,
    pygame.K_x: Button.B,
}


def event_to_input(event: pygame.event.Event) -> InputEvent | None:
    if event.type != pygame.KEYDOWN:
        return None

    button = KEYBOARD_MAP.get(event.key)
    if button is None:
        return None

    return InputEvent(button)
