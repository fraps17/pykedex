from __future__ import annotations

from PIL import ImageDraw, ImageFont


class Palette:
    BLACK = (8, 10, 14)
    PANEL = (19, 55, 55)
    PANEL_LIGHT = (117, 204, 178)
    SCREEN = (207, 227, 196)
    TEXT = (240, 247, 230)
    MUTED = (125, 155, 147)
    INK = (20, 32, 31)
    HIGHLIGHT = (190, 232, 78)
    RED = (181, 21, 38)


def font(size: int) -> ImageFont.ImageFont:
    return ImageFont.load_default()


def draw_header(draw: ImageDraw.ImageDraw, title: str, width: int = 160) -> tuple[int, int, int, int]:
    draw.rectangle((0, 0, width, 15), fill=Palette.PANEL)
    draw.line((0, 15, width, 15), fill=Palette.PANEL_LIGHT)
    draw.text((4, 4), title, fill=Palette.TEXT, font=font(13))
    return (4, 19, width - 5, 124)


def draw_text_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    max_chars: int,
    max_lines: int,
    fill: tuple[int, int, int] = Palette.INK,
) -> None:
    words = text.upper().split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)

    x, y = xy
    for index, line in enumerate(lines):
        draw.text((x, y + index * 11), line, fill=fill, font=font(12))
