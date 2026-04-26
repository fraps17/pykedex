from __future__ import annotations

import pygame

from ..input import Button, InputEvent
from .base import Palette, draw_content, font


class SettingsScreen:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size

    def handle_event(self, event: InputEvent) -> str | None:
        if event.button == Button.B:
            return "home"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        panel = draw_content(surface, "SETTINGS")
        pygame.draw.rect(surface, Palette.SCREEN, panel)
        pygame.draw.rect(surface, Palette.PANEL_LIGHT, panel, width=1)
        surface.blit(font(16).render("DISPLAY 160x128", False, Palette.INK), (16, 39))
        surface.blit(font(16).render("INPUT 6 BUTTON", False, Palette.INK), (16, 60))
        surface.blit(font(14).render("B: BACK", False, Palette.INK), (53, 95))
