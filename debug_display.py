from __future__ import annotations

from PIL import Image, ImageDraw, ImageOps

try:
    from .display import DisplayConfig, TFTDisplay
except ImportError:
    from display import DisplayConfig, TFTDisplay


def solid(size: tuple[int, int], color: tuple[int, int, int]) -> Image.Image:
    return Image.new("RGB", size, color)


def corners(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), fill=(255, 0, 0))
    draw.rectangle((width - 32, 0, width - 1, 31), fill=(0, 255, 0))
    draw.rectangle((0, height - 32, 31, height - 1), fill=(0, 0, 255))
    draw.rectangle((width - 32, height - 32, width - 1, height - 1), fill=(255, 255, 0))
    return image


def stripes(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 255),
    ]
    stripe_width = width // len(colors)
    for index, color in enumerate(colors):
        x0 = index * stripe_width
        x1 = width - 1 if index == len(colors) - 1 else x0 + stripe_width - 1
        draw.rectangle((x0, 0, x1, height - 1), fill=color)
    return image


def grid(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (8, 10, 14))
    draw = ImageDraw.Draw(image)
    for x in range(0, width, 20):
        draw.rectangle((x, 0, min(x + 2, width - 1), height - 1), fill=(180, 180, 180))
    for y in range(0, height, 20):
        draw.rectangle((0, y, width - 1, min(y + 2, height - 1)), fill=(180, 180, 180))
    draw.rectangle((0, 0, width - 1, height - 1), outline=(255, 255, 255), width=3)
    return image


def inset_borders(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
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
            (inset, inset, width - 1 - inset, height - 1 - inset),
            outline=color,
            width=4,
        )
    return image


def center_blocks(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    margin = 16
    gap = 16
    block_width = (width - margin * 2 - gap) // 2
    block_height = (height - margin * 2 - gap) // 2
    x1 = margin
    x2 = margin + block_width + gap
    y1 = margin
    y2 = margin + block_height + gap
    draw.rectangle((x1, y1, x1 + block_width, y1 + block_height), fill=(255, 0, 0))
    draw.rectangle((x2, y1, x2 + block_width, y1 + block_height), fill=(0, 255, 0))
    draw.rectangle((x1, y2, x1 + block_width, y2 + block_height), fill=(0, 0, 255))
    draw.rectangle((x2, y2, x2 + block_width, y2 + block_height), fill=(255, 255, 255))
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
    variants = [
        ("explicit 160x128", (160, 128)),
        ("explicit 128x160", (128, 160)),
    ]
    display = None

    index = 0
    while True:
        variant_name, size = variants[index % len(variants)]
        width, height = size
        if display is None or display.config.size != size:
            print(f"initializing {variant_name}")
            display = TFTDisplay(
                DisplayConfig(
                    width=width,
                    height=height,
                    scale=1,
                    swap_red_blue=False,
                    invert_colors=False,
                )
            )
            print("disp width", getattr(display.disp, "width", None))
            print("disp height", getattr(display.disp, "height", None))

        tests = [
            ("red", solid(size, (255, 0, 0))),
            ("green", solid(size, (0, 255, 0))),
            ("blue", solid(size, (0, 0, 255))),
            ("white", solid(size, (255, 255, 255))),
            ("black", solid(size, (0, 0, 0))),
            ("corners", corners(size)),
            ("stripes", stripes(size)),
            ("center blocks", center_blocks(size)),
            ("inset borders", inset_borders(size)),
            ("thick grid", grid(size)),
        ]

        print(f"variant: {variant_name}")
        for name, image in tests:
            print(f"showing {variant_name}: corrected {name}")
            transformed = transform(
                image,
                swap_red_blue=True,
                invert_colors=True,
            )
            show_raw(display, transformed)
            input("press Enter for next test...")
        index += 1


if __name__ == "__main__":
    main()
