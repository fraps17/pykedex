from __future__ import annotations

import json
import time
from typing import Protocol

from PIL import Image

try:
    from .config import Config
    from .display import Display
    from .input import Button
    from .screens.home import HomeScreen
    from .screens.pokemon_detail import PokemonDetailScreen
    from .screens.pokemon_list import PokemonListScreen
    from .screens.settings import SettingsScreen
except ImportError:
    from config import Config
    from display import Display
    from input import Button
    from screens.home import HomeScreen
    from screens.pokemon_detail import PokemonDetailScreen
    from screens.pokemon_list import PokemonListScreen
    from screens.settings import SettingsScreen


class Screen(Protocol):
    def handle_button(self, button: Button) -> str | None:
        ...

    def update(self, dt: float) -> str | None:
        ...

    def draw(self, image: Image.Image) -> None:
        ...


class PokedexApp:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.display: Display | None = None
        self.running = False
        self.pokemon = self._load_pokemon()
        self.selected_pokemon = 0
        self.current_screen: Screen = HomeScreen(config.logical_size, can_quit=not config.is_raspberry)

    def set_display(self, display: Display) -> None:
        self.display = display
        self.current_screen = HomeScreen(display.size, can_quit=not self.config.is_raspberry)

    def handle_button(self, button: Button) -> None:
        action = self.current_screen.handle_button(button)
        self._handle_action(action)

    def run(self) -> None:
        if self.display is None:
            raise RuntimeError("display must be set before running the app")

        image = Image.new("RGB", self.display.size)
        frame_time = 1 / self.config.fps
        previous = time.monotonic()
        self.running = True

        try:
            while self.running:
                start = time.monotonic()
                dt = start - previous
                previous = start

                action = self.current_screen.update(dt)
                self._handle_action(action)
                self.current_screen.draw(image)
                self.display.render(image)

                if not self.display.poll():
                    self.running = False

                elapsed = time.monotonic() - start
                time.sleep(max(0, frame_time - elapsed))
        finally:
            self.display.close()

    def _load_pokemon(self) -> list[dict[str, object]]:
        with self.config.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return list(data["pokemon"])

    def _handle_action(self, action: str | None) -> None:
        if action is None:
            return

        if action == "quit":
            self.running = False
        elif action == "home":
            self.current_screen = HomeScreen(self.display.size, can_quit=not self.config.is_raspberry)
        elif action == "pokemon_list":
            self.current_screen = PokemonListScreen(self.display.size, self.pokemon, self.selected_pokemon)
        elif action.startswith("pokemon_detail:"):
            self.selected_pokemon = int(action.split(":", 1)[1])
            self.current_screen = PokemonDetailScreen(self.display.size, self.pokemon, self.selected_pokemon)
        elif action == "settings":
            self.current_screen = SettingsScreen(self.display.size)
