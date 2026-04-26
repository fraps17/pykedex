from __future__ import annotations

from PIL import Image, ImageDraw, ImageOps

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
    draw.rectangle((0, 0, 31, 31), fill=(255, 0, 0))
    draw.rectangle((WIDTH - 32, 0, WIDTH - 1, 31), fill=(0, 255, 0))
    draw.rectangle((0, HEIGHT - 32, 31, HEIGHT - 1), fill=(0, 0, 255))
    draw.rectangle((WIDTH - 32, HEIGHT - 32, WIDTH - 1, HEIGHT - 1), fill=(255, 255, 0))
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
    for x in range(0, WIDTH, 20):
        draw.rectangle((x, 0, min(x + 2, WIDTH - 1), HEIGHT - 1), fill=(180, 180, 180))
    for y in range(0, HEIGHT, 20):
        draw.rectangle((0, y, WIDTH - 1, min(y + 2, HEIGHT - 1)), fill=(180, 180, 180))
    draw.rectangle((0, 0, WIDTH - 1, HEIGHT - 1), outline=(255, 255, 255), width=3)
    return image


def inset_borders() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [
        (255, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
    ]
    for index, color in enumerate(colors):
        inset = index * 8
        draw.rectangle(
            (inset, inset, WIDTH - 1 - inset, HEIGHT - 1 - inset),
            outline=color,
            width=4,
        )
    return image


def center_blocks() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 72, 56), fill=(255, 0, 0))
    draw.rectangle((88, 16, 144, 56), fill=(0, 255, 0))
    draw.rectangle((16, 72, 72, 112), fill=(0, 0, 255))
    draw.rectangle((88, 72, 144, 112), fill=(255, 255, 255))
    return image


def transform(image: Image.Image, *, swap_red_blue: bool, invert_colors: bool) -> Image.Image:
    if image.mode != "RGB":
        image = image.convert("RGB")
    if swap_red_blue:
        red, green, blue = image.split()
        image = Image.merge("RGB", (blue, green, red))
    if invert_colors:
        image = ImageOps.invert(image)
    return image


def show_raw(display: TFTDisplay, image: Image.Image) -> None:
    display.disp.display(image.convert("RGB"))


def main() -> None:
    display = TFTDisplay(
        DisplayConfig(
            width=WIDTH,
            height=HEIGHT,
            scale=1,
            swap_red_blue=False,
            invert_colors=False,
        )
    )
    tests = [
        ("red", solid((255, 0, 0))),
        ("green", solid((0, 255, 0))),
        ("blue", solid((0, 0, 255))),
        ("white", solid((255, 255, 255))),
        ("black", solid((0, 0, 0))),
        ("corners", corners()),
        ("stripes", stripes()),
        ("center blocks", center_blocks()),
        ("inset borders", inset_borders()),
        ("thick grid", grid()),
    ]

    index = 0
    while True:
        name, image = tests[index]
        print(f"showing corrected {name}")
        transformed = transform(
            image,
            swap_red_blue=True,
            invert_colors=True,
        )
        show_raw(display, transformed)
        input("press Enter for next test...")
        index = (index + 1) % len(tests)


if __name__ == "__main__":
    main()
