from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from ..input import Button
except ImportError:
    from input import Button
from .base import Palette, draw_header, font


class SettingsScreen:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = size

    def handle_button(self, button: Button) -> str | None:
        if button == Button.B:
            return "home"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        image.paste(Palette.BLACK, (0, 0, *self.size))
        panel = draw_header(draw, "SETTINGS", self.size[0])
        draw.rectangle(panel, fill=Palette.SCREEN, outline=Palette.PANEL_LIGHT)
        draw.text((16, 39), "DISPLAY 160x128", fill=Palette.INK, font=font(16))
        draw.text((16, 60), "INPUT 6 BUTTON", fill=Palette.INK, font=font(16))
        draw.text((53, 95), "B: BACK", fill=Palette.INK, font=font(14))
