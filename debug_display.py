from __future__ import annotations

import time

from PIL import Image, ImageDraw

try:
    from .display import DisplayConfig, TFTDisplay
except ImportError:
    from display import DisplayConfig, TFTDisplay


WIDTH = 160
HEIGHT = 128


def solid(color: tuple[int, int, int]) -> Image.Image:
    return Image.new("RGB", (WIDTH, HEIGHT), color)


def corners() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 23, 23), fill=(255, 0, 0))
    draw.rectangle((WIDTH - 24, 0, WIDTH - 1, 23), fill=(0, 255, 0))
    draw.rectangle((0, HEIGHT - 24, 23, HEIGHT - 1), fill=(0, 0, 255))
    draw.rectangle((WIDTH - 24, HEIGHT - 24, WIDTH - 1, HEIGHT - 1), fill=(255, 255, 0))
    draw.text((38, 54), "POKEDEX", fill=(255, 255, 255))
    draw.text((48, 68), "160x128", fill=(255, 255, 255))
    return image


def stripes() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 255),
    ]
    stripe_width = WIDTH // len(colors)
    for index, color in enumerate(colors):
        x0 = index * stripe_width
        x1 = WIDTH - 1 if index == len(colors) - 1 else x0 + stripe_width - 1
        draw.rectangle((x0, 0, x1, HEIGHT - 1), fill=color)
    return image


def grid() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (8, 10, 14))
    draw = ImageDraw.Draw(image)
    for x in range(0, WIDTH, 10):
        fill = (90, 90, 90) if x % 40 else (180, 180, 180)
        draw.line((x, 0, x, HEIGHT - 1), fill=fill)
    for y in range(0, HEIGHT, 10):
        fill = (90, 90, 90) if y % 40 else (180, 180, 180)
        draw.line((0, y, WIDTH - 1, y), fill=fill)
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=(255, 255, 255))
    draw.text((4, 4), "0,0", fill=(255, 255, 255))
    draw.text((118, 4), "159,0", fill=(255, 255, 255))
    draw.text((4, 116), "0,127", fill=(255, 255, 255))
    return image


def main() -> None:
    raw_config = DisplayConfig(
        width=WIDTH,
        height=HEIGHT,
        scale=1,
        swap_red_blue=False,
        invert_colors=False,
    )
    corrected_config = DisplayConfig(
        width=WIDTH,
        height=HEIGHT,
        scale=1,
        swap_red_blue=True,
        invert_colors=True,
    )
    display = TFTDisplay(raw_config)
    tests = [
        ("red", solid((255, 0, 0))),
        ("green", solid((0, 255, 0))),
        ("blue", solid((0, 0, 255))),
        ("white", solid((255, 255, 255))),
        ("black", solid((0, 0, 0))),
        ("corners", corners()),
        ("stripes", stripes()),
        ("grid", grid()),
    ]

    while True:
        print("raw output")
        display.config = raw_config
        for name, image in tests:
            print(f"showing raw {name}")
            display.render(image)
            time.sleep(2)

        print("corrected output: swap_red_blue=True, invert_colors=True")
        display.config = corrected_config
        for name, image in tests:
            print(f"showing corrected {name}")
            display.render(image)
            time.sleep(2)


if __name__ == "__main__":
    main()
