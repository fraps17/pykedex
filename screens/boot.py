from __future__ import annotations

import pygame

from ..input import Button, InputEvent
from .base import Palette, draw_shell, font


class BootScreen:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size
        self.elapsed = 0.0

    def handle_event(self, event: InputEvent) -> str | None:
        if event.button in (Button.A, Button.B):
            return "home"
        return None

    def update(self, dt: float) -> str | None:
        self.elapsed += dt
        if self.elapsed >= 1.6:
            return "home"
        return None

    def draw(self, surface: pygame.Surface) -> None:
        draw_shell(surface, "BOOT")
        panel = pygame.Rect(17, 39, 126, 65)
        pygame.draw.rect(surface, Palette.SCREEN, panel)
        pygame.draw.rect(surface, Palette.PANEL_LIGHT, panel, width=1)

        title = font(20).render("POKEDEX", False, Palette.INK)
        system = font(15).render("SYSTEM", False, Palette.INK)
        booting = font(14).render("BOOTING" + "." * (1 + int(self.elapsed * 4) % 3), False, Palette.INK)
        surface.blit(title, (45, 54))
        surface.blit(system, (56, 72))
        surface.blit(booting, (54, 91))
