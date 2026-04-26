from __future__ import annotations

from PIL import Image, ImageDraw

try:
    from .display import DisplayConfig, TFTDisplay
except ImportError:
    from display import DisplayConfig, TFTDisplay


SIZE = (160, 128)


def solid(color: tuple[int, int, int]) -> Image.Image:
    return Image.new("RGB", SIZE, color)


def stripes() -> Image.Image:
    image = Image.new("RGB", SIZE, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    for index, color in enumerate(colors):
        x0 = index * 40
        x1 = 159 if index == len(colors) - 1 else x0 + 39
        draw.rectangle((x0, 0, x1, 127), fill=color)
    return image


def corners() -> Image.Image:
    image = Image.new("RGB", SIZE, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 31, 31), fill=(255, 0, 0))
    draw.rectangle((128, 0, 159, 31), fill=(0, 255, 0))
    draw.rectangle((0, 96, 31, 127), fill=(0, 0, 255))
    draw.rectangle((128, 96, 159, 127), fill=(255, 255, 0))
    return image


def center_blocks() -> Image.Image:
    image = Image.new("RGB", SIZE, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 72, 56), fill=(255, 0, 0))
    draw.rectangle((88, 16, 144, 56), fill=(0, 255, 0))
    draw.rectangle((16, 72, 72, 112), fill=(0, 0, 255))
    draw.rectangle((88, 72, 144, 112), fill=(255, 255, 255))
    return image


def inset_borders() -> Image.Image:
    image = Image.new("RGB", SIZE, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    for index, color in enumerate(colors):
        inset = index * 8
        draw.rectangle((inset, inset, 159 - inset, 127 - inset), outline=color, width=4)
    return image


def main() -> None:
    display = TFTDisplay(DisplayConfig(width=160, height=128, scale=1))
    print("disp public width", getattr(display.disp, "width", None))
    print("disp public height", getattr(display.disp, "height", None))
    print("disp internal _width", getattr(display.disp, "_width", None))
    print("disp internal _height", getattr(display.disp, "_height", None))
    print("disp rotation", getattr(display.disp, "_rotation", None))
    print("disp offset_left", getattr(display.disp, "_offset_left", None))
    print("disp offset_top", getattr(display.disp, "_offset_top", None))

    tests = [
        ("red", solid((255, 0, 0))),
        ("green", solid((0, 255, 0))),
        ("blue", solid((0, 0, 255))),
        ("white", solid((255, 255, 255))),
        ("black", solid((0, 0, 0))),
        ("stripes", stripes()),
        ("corners", corners()),
        ("center blocks", center_blocks()),
        ("inset borders", inset_borders()),
    ]

    index = 0
    while True:
        name, image = tests[index]
        print(f"showing {name}, image size {image.size}")
        display.render(image)
        input("press Enter for next test...")
        index = (index + 1) % len(tests)


if __name__ == "__main__":
    main()
