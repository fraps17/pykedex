from __future__ import annotations

import pygame
import ST7735
from PIL import Image


WIDTH = 160
HEIGHT = 128

disp = ST7735.ST7735(
    port=0,
    cs=0,
    dc=24,
    rst=25,
    spi_speed_hz=4000000,
)
disp.begin()


def render(surface: pygame.Surface) -> None:
    rgb = pygame.image.tostring(surface, "RGB")
    image = Image.frombytes("RGB", surface.get_size(), rgb)
    disp.display(image)
