from __future__ import annotations

from enum import Enum, auto
import time
from typing import Callable


class Button(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    A = auto()
    B = auto()


ButtonHandler = Callable[[Button], None]


class GPIOInput:
    PIN_TO_BUTTON = {
        17: Button.UP,
        27: Button.DOWN,
        22: Button.B,
        23: Button.A,
    }

    def __init__(self, on_button: ButtonHandler, debounce_seconds: float = 0.18) -> None:
        try:
            import gpiod
        except ImportError as error:
            raise RuntimeError("GPIO input requires python gpiod on Raspberry Pi") from error

        self.on_button = on_button
        self.debounce_seconds = debounce_seconds
        self.gpiod = gpiod
        self.last_pressed_at = {pin: 0.0 for pin in self.PIN_TO_BUTTON}
        self.previous_values: dict[int, int] = {}
        self.requests = []

        chip = self._find_gpiochip()
        for pin in self.PIN_TO_BUTTON:
            request = gpiod.request_lines(
                chip,
                consumer=f"pokedex-button-{pin}",
                config={
                    pin: gpiod.LineSettings(
                        direction=gpiod.line.Direction.INPUT,
                        bias=gpiod.line.Bias.PULL_UP,
                    )
                },
            )
            self.requests.append(request)
            self.previous_values[pin] = self._read_pin(request, pin)

    def poll(self) -> None:
        now = time.monotonic()
        for request, pin in zip(self.requests, self.PIN_TO_BUTTON):
            value = self._read_pin(request, pin)
            previous = self.previous_values[pin]
            self.previous_values[pin] = value

            if previous == 1 and value == 0 and now - self.last_pressed_at[pin] >= self.debounce_seconds:
                self.last_pressed_at[pin] = now
                self.on_button(self.PIN_TO_BUTTON[pin])

    def close(self) -> None:
        for request in self.requests:
            release = getattr(request, "release", None)
            if callable(release):
                release()

    def _read_pin(self, request: object, pin: int) -> int:
        value = request.get_value(pin)
        if hasattr(value, "value"):
            return int(value.value)
        return int(value)

    def _find_gpiochip(self) -> str:
        for chip in ("/dev/gpiochip4", "/dev/gpiochip0"):
            try:
                request = self.gpiod.request_lines(
                    chip,
                    consumer="pokedex-button-probe",
                    config={
                        17: self.gpiod.LineSettings(
                            direction=self.gpiod.line.Direction.INPUT,
                            bias=self.gpiod.line.Bias.PULL_UP,
                        )
                    },
                )
            except OSError:
                continue
            release = getattr(request, "release", None)
            if callable(release):
                release()
            return chip
        raise RuntimeError("No usable GPIO chip found for buttons")
