from __future__ import annotations

import time

try:
    from .input import Button, GPIOInput
except ImportError:
    from input import Button, GPIOInput


def on_button(button: Button) -> None:
    print(button.name)


def main() -> None:
    buttons = GPIOInput(on_button)
    print("Listening for buttons. Press Ctrl+C to stop.")
    try:
        while True:
            buttons.poll()
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass
    finally:
        buttons.close()


if __name__ == "__main__":
    main()
