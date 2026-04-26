from __future__ import annotations

import pygame

from ..input import Button, InputEvent
from .base import Palette, draw_content, font


class PokemonListScreen:
    def __init__(self, size: tuple[int, int], pokemon: list[dict[str, object]], selected: int = 0) -> None:
        self.size = size
        self.pokemon = pokemon
        self.selected = selected

    def handle_event(self, event: InputEvent) -> str | None:
        if event.button == Button.UP:
            self.selected = (self.selected - 1) % len(self.pokemon)
        elif event.button == Button.DOWN:
            self.selected = (self.selected + 1) % len(self.pokemon)
        elif event.button == Button.A:
            return f"pokemon_detail:{self.selected}"
        elif event.button == Button.B:
            return "home"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        panel = draw_content(surface, "POKEMON")
        pygame.draw.rect(surface, Palette.PANEL, panel)
        pygame.draw.rect(surface, Palette.PANEL_LIGHT, panel, width=1)

        start = max(0, min(self.selected - 3, max(0, len(self.pokemon) - 7)))
        visible = self.pokemon[start : start + 7]
        for offset, pokemon in enumerate(visible):
            index = start + offset
            y = panel.y + 5 + offset * 14
            if index == self.selected:
                pygame.draw.rect(surface, Palette.HIGHLIGHT, (panel.x + 5, y - 3, panel.width - 10, 12))
                color = Palette.INK
            else:
                color = Palette.TEXT

            number = int(pokemon["id"])
            name = str(pokemon["name"]).upper()
            surface.blit(font(14).render(f"{number:03d} {name}", False, color), (panel.x + 10, y))
