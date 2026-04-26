from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from ..input import Button
except ImportError:
    from input import Button
from .base import Palette, draw_header, font


class PokemonListScreen:
    def __init__(self, size: tuple[int, int], pokemon: list[dict[str, object]], selected: int = 0) -> None:
        self.size = size
        self.pokemon = pokemon
        self.selected = selected

    def handle_button(self, button: Button) -> str | None:
        if button == Button.UP:
            self.selected = (self.selected - 1) % len(self.pokemon)
        elif button == Button.DOWN:
            self.selected = (self.selected + 1) % len(self.pokemon)
        elif button == Button.A:
            return f"pokemon_detail:{self.selected}"
        elif button == Button.B:
            return "home"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        image.paste(Palette.BLACK, (0, 0, *self.size))
        panel = draw_header(draw, "POKEMON", self.size[0])
        draw.rectangle(panel, fill=Palette.PANEL, outline=Palette.PANEL_LIGHT)

        start = max(0, min(self.selected - 3, max(0, len(self.pokemon) - 7)))
        visible = self.pokemon[start : start + 7]
        for offset, pokemon in enumerate(visible):
            index = start + offset
            y = panel[1] + 5 + offset * 14
            if index == self.selected:
                draw.rectangle((panel[0] + 5, y - 3, panel[2] - 5, y + 9), fill=Palette.HIGHLIGHT)
                color = Palette.INK
            else:
                color = Palette.TEXT

            number = int(pokemon["id"])
            name = str(pokemon["name"]).upper()
            draw.text((panel[0] + 10, y), f"{number:03d} {name}", fill=color, font=font(14))
