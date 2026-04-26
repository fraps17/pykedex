from __future__ import annotations

import json
from typing import Protocol

import pygame

from .config import Config
from . import display
from .input import InputEvent
from .screens.boot import BootScreen
from .screens.home import HomeScreen
from .screens.pokemon_detail import PokemonDetailScreen
from .screens.pokemon_list import PokemonListScreen
from .screens.settings import SettingsScreen


class Screen(Protocol):
    def handle_event(self, event: InputEvent) -> str | None:
        ...

    def update(self, dt: float) -> str | None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        ...


class PokedexApp:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.running = False
        self.clock: pygame.time.Clock | None = None
        self.canvas: pygame.Surface | None = None
        self.pokemon = self._load_pokemon()
        self.selected_pokemon = 0
        self.current_screen: Screen = BootScreen(config.logical_size)

    def run(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.canvas = pygame.Surface(self.config.logical_size)

        self.running = True
        try:
            while self.running:
                dt = self.clock.tick(self.config.fps) / 1000.0
                action = self.current_screen.update(dt)
                self._handle_action(action)
                self._draw()
        finally:
            pygame.quit()

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
            self.current_screen = HomeScreen(self.config.logical_size)
        elif action == "pokemon_list":
            self.current_screen = PokemonListScreen(self.config.logical_size, self.pokemon, self.selected_pokemon)
        elif action.startswith("pokemon_detail:"):
            self.selected_pokemon = int(action.split(":", 1)[1])
            self.current_screen = PokemonDetailScreen(
                self.config.logical_size,
                self.pokemon,
                self.selected_pokemon,
            )
        elif action == "settings":
            self.current_screen = SettingsScreen(self.config.logical_size)

    def _draw(self) -> None:
        if self.canvas is None:
            return

        self.current_screen.draw(self.canvas)
        display.render(self.canvas)
