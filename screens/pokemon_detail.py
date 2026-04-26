from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from ..input import Button
except ImportError:
    from input import Button
from .base import Palette, draw_header, draw_text_lines, font


SECTIONS = ("INFO", "STATS")


class PokemonDetailScreen:
    def __init__(self, size: tuple[int, int], pokemon: list[dict[str, object]], selected: int) -> None:
        self.size = size
        self.pokemon = pokemon
        self.selected = selected
        self.section = 0

    def handle_button(self, button: Button) -> str | None:
        if button == Button.LEFT:
            self.section = (self.section - 1) % len(SECTIONS)
        elif button == Button.RIGHT:
            self.section = (self.section + 1) % len(SECTIONS)
        elif button == Button.UP:
            self.selected = (self.selected - 1) % len(self.pokemon)
        elif button == Button.DOWN:
            self.selected = (self.selected + 1) % len(self.pokemon)
        elif button == Button.B:
            return "pokemon_list"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        image.paste(Palette.BLACK, (0, 0, *self.size))
        pokemon = self.pokemon[self.selected]
        number = int(pokemon["id"])
        title = f"{number:03d} {str(pokemon['name']).upper()}"
        panel = draw_header(draw, title, self.size[0])
        draw.rectangle(panel, fill=Palette.SCREEN, outline=Palette.PANEL_LIGHT)
        draw.text((126, 22), SECTIONS[self.section], fill=Palette.INK, font=font(13))

        self._draw_sprite(draw, panel, pokemon)
        if self.section == 0:
            self._draw_info(draw, pokemon)
        else:
            self._draw_stats(draw, pokemon)

    def _draw_sprite(self, draw: ImageDraw.ImageDraw, panel: tuple[int, int, int, int], pokemon: dict[str, object]) -> None:
        types = list(pokemon["types"])
        color = self._type_color(str(types[0]))
        center = (panel[0] + 21, panel[1] + 21)
        draw.ellipse((center[0] - 15, center[1] - 15, center[0] + 15, center[1] + 15), fill=color, outline=Palette.INK)
        draw.ellipse((center[0] - 7, center[1] - 5, center[0] - 3, center[1] - 1), fill=Palette.INK)
        draw.ellipse((center[0] + 3, center[1] - 5, center[0] + 7, center[1] - 1), fill=Palette.INK)
        draw.arc((center[0] - 8, center[1] - 3, center[0] + 8, center[1] + 9), 10, 170, fill=Palette.INK)

    def _draw_info(self, draw: ImageDraw.ImageDraw, pokemon: dict[str, object]) -> None:
        types = "/".join(str(item).upper() for item in pokemon["types"])
        height = pokemon["height"]
        weight = pokemon["weight"]
        draw.text((50, 40), types, fill=Palette.INK, font=font(13))
        draw.text((50, 53), f"HT {height}m  WT {weight}kg", fill=Palette.INK, font=font(13))
        draw_text_lines(draw, str(pokemon["description"]), (10, 79), max_chars=25, max_lines=4)

    def _draw_stats(self, draw: ImageDraw.ImageDraw, pokemon: dict[str, object]) -> None:
        stats = dict(pokemon["stats"])
        y = 42
        for label in ("HP", "ATK", "DEF"):
            value = int(stats[label.lower()])
            draw.text((50, y), label, fill=Palette.INK, font=font(14))
            draw.rectangle((79, y + 3, 139, y + 9), fill=(116, 135, 118))
            draw.rectangle((79, y + 3, 79 + min(60, value // 2), y + 9), fill=Palette.RED)
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
