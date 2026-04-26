from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from ..input import Button
except ImportError:
    from input import Button
from .base import Palette, draw_header, font


MENU_ITEMS = [
    ("Pokemon", "pokemon_list"),
    ("Search", None),
    ("Settings", "settings"),
    ("Shutdown", "quit"),
]


class HomeScreen:
    def __init__(self, size: tuple[int, int], can_quit: bool = True) -> None:
        self.size = size
        self.can_quit = can_quit
        self.selected = 0

    def handle_button(self, button: Button) -> str | None:
        if button == Button.UP:
            self.selected = (self.selected - 1) % len(MENU_ITEMS)
        elif button == Button.DOWN:
            self.selected = (self.selected + 1) % len(MENU_ITEMS)
        elif button == Button.A:
            action = MENU_ITEMS[self.selected][1]
            if action == "quit" and not self.can_quit:
                return None
            return action
        elif button == Button.B:
            if not self.can_quit:
                return None
            return "quit"
        return None

    def update(self, dt: float) -> str | None:
        return None

    def draw(self, image: Image.Image) -> None:
        draw = ImageDraw.Draw(image)
        image.paste(Palette.BLACK, (0, 0, *self.size))
        panel = draw_header(draw, "HOME", self.size[0])
        draw.rectangle(panel, fill=Palette.PANEL, outline=Palette.PANEL_LIGHT)

        for index, (label, action) in enumerate(MENU_ITEMS):
            y = panel[1] + 9 + index * 20
            if index == self.selected:
                draw.rectangle((panel[0] + 5, y - 4, panel[2] - 5, y + 12), fill=Palette.HIGHLIGHT)
                color = Palette.INK
            else:
                color = Palette.TEXT if action is not None else Palette.MUTED
            draw.text((panel[0] + 12, y), label.upper(), fill=color, font=font(18))
