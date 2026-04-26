from __future__ import annotations

import pygame

from ..input import Button, InputEvent
from .base import Palette, draw_content, font


SECTIONS = ("INFO", "STATS")


class PokemonDetailScreen:
    def __init__(self, size: tuple[int, int], pokemon: list[dict[str, object]], selected: int) -> None:
        self.size = size
        self.pokemon = pokemon
        self.selected = selected
        self.section = 0

    def handle_event(self, event: InputEvent) -> str | None:
        if event.button == Button.LEFT:
            self.section = (self.section - 1) % len(SECTIONS)
        elif event.button == Button.RIGHT:
            self.section = (self.section + 1) % len(SECTIONS)
        elif event.button == Button.UP:
            self.selected = (self.selected - 1) % len(self.pokemon)
        elif event.button == Button.DOWN:
            self.selected = (self.selected + 1) % len(self.pokemon)
        elif event.button == Button.B:
            return "pokemon_list"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, surface: pygame.Surface) -> None:
        pokemon = self.pokemon[self.selected]
        number = int(pokemon["id"])
        title = f"{number:03d} {str(pokemon['name']).upper()}"
        panel = draw_content(surface, title)
        pygame.draw.rect(surface, Palette.SCREEN, panel)
        pygame.draw.rect(surface, Palette.PANEL_LIGHT, panel, width=1)

        self._draw_sprite(surface, panel, pokemon)
        surface.blit(font(13).render(SECTIONS[self.section], False, Palette.INK), (126, 22))

        if self.section == 0:
            self._draw_info(surface, pokemon)
        else:
            self._draw_stats(surface, pokemon)

    def _draw_sprite(self, surface: pygame.Surface, panel: pygame.Rect, pokemon: dict[str, object]) -> None:
        types = list(pokemon["types"])
        color = self._type_color(str(types[0]))
        center = (panel.x + 21, panel.y + 21)
        pygame.draw.circle(surface, color, center, 15)
        pygame.draw.circle(surface, Palette.INK, (center[0] - 5, center[1] - 3), 2)
        pygame.draw.circle(surface, Palette.INK, (center[0] + 5, center[1] - 3), 2)
        pygame.draw.arc(surface, Palette.INK, (center[0] - 7, center[1] - 2, 14, 9), 0.2, 2.9, 1)

    def _draw_info(self, surface: pygame.Surface, pokemon: dict[str, object]) -> None:
        types = "/".join(str(item).upper() for item in pokemon["types"])
        height = pokemon["height"]
        weight = pokemon["weight"]
        surface.blit(font(13).render(types, False, Palette.INK), (50, 40))
        surface.blit(font(13).render(f"HT {height}m  WT {weight}kg", False, Palette.INK), (50, 53))
        description = str(pokemon["description"]).upper()
        surface.blit(font(12).render(description[:25], False, Palette.INK), (10, 79))
        surface.blit(font(12).render(description[25:50], False, Palette.INK), (10, 91))
        surface.blit(font(12).render(description[50:75], False, Palette.INK), (10, 103))

    def _draw_stats(self, surface: pygame.Surface, pokemon: dict[str, object]) -> None:
        stats = dict(pokemon["stats"])
        y = 42
        for label in ("HP", "ATK", "DEF"):
            value = int(stats[label.lower()])
            surface.blit(font(14).render(label, False, Palette.INK), (50, y))
            pygame.draw.rect(surface, (116, 135, 118), (79, y + 3, 60, 6))
            pygame.draw.rect(surface, Palette.RED, (79, y + 3, min(60, value // 2), 6))
            y += 18

    def _type_color(self, type_name: str) -> tuple[int, int, int]:
        return {
            "Bug": (139, 184, 63),
            "Dragon": (111, 99, 213),
            "Electric": (239, 206, 56),
            "Fairy": (229, 136, 198),
            "Fighting": (195, 82, 61),
            "Fire": (230, 91, 48),
            "Flying": (134, 169, 229),
            "Ghost": (106, 88, 154),
            "Water": (74, 146, 219),
            "Grass": (84, 181, 91),
            "Ground": (211, 170, 88),
            "Ice": (103, 201, 208),
            "Poison": (155, 92, 181),
            "Normal": (188, 176, 145),
            "Psychic": (228, 91, 143),
            "Rock": (176, 153, 91),
            "Steel": (151, 166, 177),
        }.get(type_name, (150, 180, 160))
