from __future__ import annotations

from collections.abc import Callable

from PIL import Image, ImageDraw, ImageOps

try:
    from .display import DisplayConfig, TFTDisplay
except ImportError:
    from display import DisplayConfig, TFTDisplay


LOGICAL_SIZE = (160, 128)


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


def corners(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), fill=(255, 0, 0))
    draw.rectangle((width - 32, 0, width - 1, 31), fill=(0, 255, 0))
    draw.rectangle((0, height - 32, 31, height - 1), fill=(0, 0, 255))
    draw.rectangle((width - 32, height - 32, width - 1, height - 1), fill=(255, 255, 0))
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


def correct_colors(image: Image.Image) -> Image.Image:
    if image.mode != "RGB":
        image = image.convert("RGB")
    red, green, blue = image.split()
    return ImageOps.invert(Image.merge("RGB", (blue, green, red)))


def identity(image: Image.Image) -> Image.Image:
    return image


def rotate_90(image: Image.Image) -> Image.Image:
    return image.transpose(Image.Transpose.ROTATE_90)


def rotate_180(image: Image.Image) -> Image.Image:
    return image.transpose(Image.Transpose.ROTATE_180)


def rotate_270(image: Image.Image) -> Image.Image:
    return image.transpose(Image.Transpose.ROTATE_270)


def flip_left_right(image: Image.Image) -> Image.Image:
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def flip_top_bottom(image: Image.Image) -> Image.Image:
    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)


def send(display: TFTDisplay, image: Image.Image) -> None:
    image = correct_colors(image)
    print("sending image size", image.size)
    display.disp.display(image)


def main() -> None:
    display = TFTDisplay(
        DisplayConfig(
            width=160,
            height=128,
            scale=1,
            swap_red_blue=False,
            invert_colors=False,
        )
    )
    print("disp public width", getattr(display.disp, "width", None))
    print("disp public height", getattr(display.disp, "height", None))
    print("disp internal _width", getattr(display.disp, "_width", None))
    print("disp internal _height", getattr(display.disp, "_height", None))
    print("disp rotation", getattr(display.disp, "_rotation", None))
    print("disp offset_left", getattr(display.disp, "_offset_left", None))
    print("disp offset_top", getattr(display.disp, "_offset_top", None))

    source_patterns = [
        ("stripes", stripes),
        ("corners", corners),
        ("center blocks", center_blocks),
    ]
    transforms: list[tuple[str, Callable[[Image.Image], Image.Image]]] = [
        ("identity", identity),
        ("rotate 90", rotate_90),
        ("rotate 180", rotate_180),
        ("rotate 270", rotate_270),
        ("flip left/right", flip_left_right),
        ("flip top/bottom", flip_top_bottom),
    ]

    while True:
        for pattern_name, make_pattern in source_patterns:
            base = make_pattern(LOGICAL_SIZE)
            for transform_name, transform in transforms:
                image = transform(base)
                print(f"pattern={pattern_name} transform={transform_name}")
                send(display, image)
                input("press Enter for next test...")


if __name__ == "__main__":
    main()
