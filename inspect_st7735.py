from __future__ import annotations

import inspect

try:
    import st7735 as ST7735
except ImportError:
    import ST7735

from display import DisplayConfig, TFTDisplay


def main() -> None:
    print("ST7735 module:", getattr(ST7735, "__file__", None))
    print("ST7735 class:", ST7735.ST7735)
    print("ST7735 init signature:", inspect.signature(ST7735.ST7735))
    print()

    display = TFTDisplay(
        DisplayConfig(
            width=160,
            height=128,
            scale=1,
            swap_red_blue=False,
            invert_colors=False,
        )
    )
    disp = display.disp

    print("driver object:", disp)
    print("driver width:", getattr(disp, "width", None))
    print("driver height:", getattr(disp, "height", None))
    print("driver attributes:")
    for key, value in sorted(getattr(disp, "__dict__", {}).items()):
        print(f"  {key}: {value!r}")
    print()

    for name in [
        "display",
        "set_window",
        "command",
        "data",
        "begin",
        "_set_window",
        "_display",
    ]:
        value = getattr(disp, name, None)
        if value is None:
            continue
        print(f"{name} signature:", end=" ")
        try:
            print(inspect.signature(value))
        except (TypeError, ValueError):
            print("<unavailable>")
        try:
            print(inspect.getsource(value))
        except (OSError, TypeError):
            print("<source unavailable>")
        print()


if __name__ == "__main__":
    main()
