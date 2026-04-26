from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

from PIL import Image, ImageOps

try:
    from .input import Button
except ImportError:
    from input import Button


ButtonHandler = Callable[[Button], None]


class Display(Protocol):
    def render(self, image: Image.Image) -> None:
        ...

    def poll(self) -> bool:
        ...

    def close(self) -> None:
        ...


@dataclass(frozen=True)
class DisplayConfig:
    width: int = 160
    height: int = 128
    scale: int = 4
    swap_red_blue: bool = True
    invert_colors: bool = True

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class TFTDisplay:
    def __init__(self, config: DisplayConfig) -> None:
        import ST7735

        self.config = config
        kwargs = {
            "port": 0,
            "cs": ST7735.BG_SPI_CS_BACK,
            "dc": "GPIO24",
            "rst": "GPIO25",
            "backlight": "GPIO18",
            "rotation": 90,
            "spi_speed_hz": 4000000,
            "width": config.width,
            "height": config.height,
        }
        try:
            self.disp = ST7735.ST7735(**kwargs)
        except TypeError:
            kwargs.pop("width")
            kwargs.pop("height")
            self.disp = ST7735.ST7735(**kwargs)
        self.disp.begin()

    def render(self, image: Image.Image) -> None:
        if image.mode != "RGB":
            image = image.convert("RGB")
        if self.config.swap_red_blue:
            red, green, blue = image.split()
            image = Image.merge("RGB", (blue, green, red))
        if self.config.invert_colors:
            image = ImageOps.invert(image)
        self.disp.display(image)

    def poll(self) -> bool:
        return True

    def close(self) -> None:
        pass


class WindowDisplay:
    def __init__(self, config: DisplayConfig, on_button: ButtonHandler | None = None) -> None:
        import pyglet

        self.config = config
        self.on_button = on_button
        self.closed = False
        self.pyglet = pyglet
        self.window = pyglet.window.Window(
            width=self.config.width * self.config.scale,
            height=self.config.height * self.config.scale,
            caption="Pokedex",
            resizable=False,
        )
        self.sprite: pyglet.sprite.Sprite | None = None
        self.window.push_handlers(
            on_close=self._on_close,
            on_key_press=self._on_key_press,
            on_text=self._on_text,
        )

    def render(self, image: Image.Image) -> None:
        if image.mode != "RGB":
            image = image.convert("RGB")
        flipped = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        image_data = self.pyglet.image.ImageData(
            self.config.width,
            self.config.height,
            "RGB",
            flipped.tobytes(),
            pitch=self.config.width * 3,
        )
        texture = image_data.get_texture()
        if self.sprite is None:
            self.sprite = self.pyglet.sprite.Sprite(texture)
            self.sprite.scale = self.config.scale
        else:
            self.sprite.image = texture

        self.window.switch_to()
        self.window.dispatch_events()
        self.window.clear()
        self.sprite.draw()
        self.window.flip()

    def poll(self) -> bool:
        return not self.closed

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        self.window.close()

    def _on_close(self) -> None:
        self.closed = True

    def _on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        key = self.pyglet.window.key
        keymap = {
            key.UP: Button.UP,
            key.DOWN: Button.DOWN,
            key.LEFT: Button.LEFT,
            key.RIGHT: Button.RIGHT,
            key.ENTER: Button.A,
            key.RETURN: Button.A,
            key.Z: Button.A,
            key.ESCAPE: Button.B,
            key.X: Button.B,
        }
        button = keymap.get(symbol)
        if button is None:
            return None
        self._send_button(button)
        return self.pyglet.event.EVENT_HANDLED

    def _on_text(self, text: str) -> bool | None:
        keymap = {
            "z": Button.A,
            "Z": Button.A,
            "x": Button.B,
            "X": Button.B,
        }
        button = keymap.get(text)
        if button is None:
            return None
        self._send_button(button)
        return self.pyglet.event.EVENT_HANDLED

    def _send_button(self, button: Button) -> None:
        if self.on_button is not None:
            self.on_button(button)


def create_display(is_raspberry: bool, config: DisplayConfig, on_button: ButtonHandler | None = None) -> Display:
    if is_raspberry:
        return TFTDisplay(config)
    return WindowDisplay(config, on_button)
