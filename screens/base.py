from __future__ import annotations

import pygame


class Palette:
    RED = (181, 21, 38)
    DARK_RED = (86, 8, 22)
    BLACK = (8, 10, 14)
    PANEL = (19, 55, 55)
    PANEL_LIGHT = (117, 204, 178)
    SCREEN = (207, 227, 196)
    TEXT = (240, 247, 230)
    INK = (20, 32, 31)
    HIGHLIGHT = (190, 232, 78)


def font(size: int) -> pygame.font.Font:
    return pygame.font.Font(None, size)


def draw_shell(surface: pygame.Surface, title: str) -> None:
    width, height = surface.get_size()
    surface.fill(Palette.DARK_RED)
    pygame.draw.rect(surface, Palette.RED, (2, 2, width - 4, height - 4), border_radius=5)
    pygame.draw.rect(surface, (43, 4, 14), (2, 2, width - 4, height - 4), width=2, border_radius=5)
    pygame.draw.circle(surface, (139, 225, 255), (17, 15), 7)
    pygame.draw.circle(surface, (245, 255, 255), (15, 13), 3)
    pygame.draw.circle(surface, (34, 45, 55), (17, 15), 7, width=1)
    for index, color in enumerate(((252, 63, 64), (252, 205, 68), (69, 212, 101))):
        pygame.draw.circle(surface, color, (35 + index * 10, 11), 3)

    label = font(13).render(title, False, Palette.TEXT)
    surface.blit(label, (82, 8))
    pygame.draw.rect(surface, Palette.BLACK, (9, 28, width - 18, height - 37), border_radius=3)


def draw_content(surface: pygame.Surface, title: str) -> pygame.Rect:
    width, height = surface.get_size()
    surface.fill(Palette.BLACK)
    pygame.draw.rect(surface, Palette.PANEL, (0, 0, width, 15))
    pygame.draw.line(surface, Palette.PANEL_LIGHT, (0, 15), (width, 15))
    surface.blit(font(13).render(title, False, Palette.TEXT), (4, 4))
    return pygame.Rect(4, 19, width - 8, height - 23)
