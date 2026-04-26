from __future__ import annotations

import pygame

from ..input import Button, InputEvent
from .base import Palette, draw_content, font


MENU_ITEMS = [
    ("Pokemon", "pokemon_list"),
    ("Search", None),
    ("Settings", "settings"),
    ("Shutdown", "quit"),
]


class HomeScreen:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.selected = 0

    def handle_event(self, event: InputEvent) -> str | None:
        if event.button == Button.UP:
            self.selected = (self.selected - 1) % len(MENU_ITEMS)
        elif event.button == Button.DOWN:
            self.selected = (self.selected + 1) % len(MENU_ITEMS)
        elif event.button == Button.A:
            return MENU_ITEMS[self.selected][1]
        elif event.button == Button.B:
            return "quit"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        panel = draw_content(surface, "HOME")
        pygame.draw.rect(surface, Palette.PANEL, panel)
        pygame.draw.rect(surface, Palette.PANEL_LIGHT, panel, width=1)

        for index, (label, action) in enumerate(MENU_ITEMS):
            y = panel.y + 9 + index * 20
            if index == self.selected:
                pygame.draw.rect(surface, Palette.HIGHLIGHT, (panel.x + 5, y - 4, panel.width - 10, 16))
                color = Palette.INK
            else:
                color = Palette.TEXT if action is not None else (125, 155, 147)
            surface.blit(font(18).render(label.upper(), False, color), (panel.x + 12, y))
