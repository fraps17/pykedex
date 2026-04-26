from __future__ import annotations

import argparse

from .config import Config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Pokédex pygame app.")
    parser.add_argument("--fullscreen", action="store_true", help="start in fullscreen Raspberry Pi mode")
    parser.add_argument("--scale", type=int, default=4, help="development window scale")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = Config(fullscreen=args.fullscreen, scale=args.scale)

    from .app import PokedexApp

    PokedexApp(config).run()


if __name__ == "__main__":
    main()
