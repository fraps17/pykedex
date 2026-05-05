from __future__ import annotations

import argparse

if __package__ in (None, ""):
    from app import PokedexApp
    from config import Config
    from display import DisplayConfig, create_display
else:
    from .app import PokedexApp
    from .config import Config
    from .display import DisplayConfig, create_display


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Pokédex app.")
    return parser.parse_args()


def main() -> None:
    parse_args()
    config = Config.from_env()
    app = PokedexApp(config)
    display = create_display(
        config.is_raspberry,
        DisplayConfig(width=config.logical_width, height=config.logical_height, scale=config.scale),
        app.handle_button,
    )
    app.set_display(display)
    app.run()


if __name__ == "__main__":
    main()
