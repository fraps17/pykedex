from __future__ import annotations

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageOps


try:
    import st7735 as ST7735
except ImportError:
    import ST7735


LOGICAL_SIZE = (160, 128)


@dataclass(frozen=True)
class Variant:
    name: str
    width: int
    height: int
    rotation: int
    offset_left: int | None = None
    offset_top: int | None = None


def stripes(size: tuple[int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(image)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
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


def corrected(image: Image.Image) -> Image.Image:
    red, green, blue = image.convert("RGB").split()
    return ImageOps.invert(Image.merge("RGB", (blue, green, red)))


def make_display(variant: Variant) -> object:
    kwargs = {
        "port": 0,
        "cs": ST7735.BG_SPI_CS_BACK,
        "dc": "GPIO24",
        "rst": "GPIO25",
        "backlight": "GPIO18",
        "width": variant.width,
        "height": variant.height,
        "rotation": variant.rotation,
        "invert": True,
        "bgr": True,
        "spi_speed_hz": 4000000,
    }
    if variant.offset_left is not None:
        kwargs["offset_left"] = variant.offset_left
    if variant.offset_top is not None:
        kwargs["offset_top"] = variant.offset_top
    return ST7735.ST7735(**kwargs)


def print_display_info(display: object) -> None:
    print("public width", getattr(display, "width", None))
    print("public height", getattr(display, "height", None))
    print("internal _width", getattr(display, "_width", None))
    print("internal _height", getattr(display, "_height", None))
    print("rotation", getattr(display, "_rotation", None))
    print("offset_left", getattr(display, "_offset_left", None))
    print("offset_top", getattr(display, "_offset_top", None))
    print("invert", getattr(display, "_invert", None))
    print("bgr", getattr(display, "_bgr", None))


def image_size_for(display: object) -> tuple[int, int]:
    return (
        int(getattr(display, "width")),
        int(getattr(display, "height")),
    )


def main() -> None:
    variants = [
        Variant("160x128 rot0 default offsets", 160, 128, 0),
        Variant("160x128 rot90 default offsets", 160, 128, 90),
        Variant("128x160 rot90 default offsets", 128, 160, 90),
        Variant("128x160 rot0 default offsets", 128, 160, 0),
        Variant("160x128 rot0 offsets 0,0", 160, 128, 0, 0, 0),
        Variant("160x128 rot90 offsets 0,0", 160, 128, 90, 0, 0),
        Variant("128x160 rot90 offsets 0,0", 128, 160, 90, 0, 0),
        Variant("128x160 rot0 offsets 0,0", 128, 160, 0, 0, 0),
    ]

    for variant in variants:
        print()
        print("=" * 60)
        print(variant.name)
        display = make_display(variant)
        print_display_info(display)
        size = image_size_for(display)

        for pattern_name, image in [
            ("stripes", stripes(size)),
            ("corners", corners(size)),
        ]:
            print(f"showing {pattern_name}, image size {image.size}")
            display.display(corrected(image))
            input("press Enter for next pattern...")

        input("press Enter for next variant...")


if __name__ == "__main__":
    main()
