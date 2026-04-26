from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from ..input import Button
except ImportError:
    from input import Button
from .base import Palette, draw_header, font


class BootScreen:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size

    def handle_button(self, button: Button) -> str | None:
        return "home"

    def update(self, dt: float) -> str | None:
        return "home"

    def draw(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        image.paste(Palette.BLACK, (0, 0, *self.size))
        draw_header(draw, "BOOT", self.size[0])
        draw.rectangle((17, 39, 143, 104), fill=Palette.SCREEN, outline=Palette.PANEL_LIGHT)
        draw.text((45, 55), "POKEDEX", fill=Palette.INK, font=font(20))
        draw.text((57, 72), "SYSTEM", fill=Palette.INK, font=font(15))
        draw.text((55, 91), "BOOTING", fill=Palette.INK, font=font(14))
