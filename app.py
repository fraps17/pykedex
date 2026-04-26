from __future__ import annotations

import json
from typing import Protocol

import pygame

from .config import Config
from .input import Button, InputEvent, event_to_input
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
        self.display: pygame.Surface | None = None
        self.canvas: pygame.Surface | None = None
        self.pokemon = self._load_pokemon()
        self.selected_pokemon = 0
        self.current_screen: Screen = BootScreen(config.logical_size)

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Pokédex")
        pygame.mouse.set_visible(False)

        self.clock = pygame.time.Clock()
        self.display = self._create_display()
        self.canvas = pygame.Surface(self.config.logical_size).convert()

        self.running = True
        try:
            while self.running:
                dt = self.clock.tick(self.config.fps) / 1000.0
                self._handle_pygame_events()
                action = self.current_screen.update(dt)
                self._handle_action(action)
                self._draw()
        finally:
            pygame.quit()

    def _load_pokemon(self) -> list[dict[str, object]]:
        with self.config.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return list(data["pokemon"])

    def _create_display(self) -> pygame.Surface:
        if self.config.fullscreen:
            return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        return pygame.display.set_mode(self.config.window_size)

    def _handle_pygame_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                continue

            input_event = event_to_input(event)
            if input_event is None:
                continue

            action = self.current_screen.handle_event(input_event)
            self._handle_action(action)

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
        if self.canvas is None or self.display is None:
            return

        self.current_screen.draw(self.canvas)
        self.display.fill((5, 6, 8))
        target = self._scaled_rect(self.display.get_size())
        scaled = pygame.transform.scale(self.canvas, target.size)
        self.display.blit(scaled, target)
        pygame.display.flip()

    def _scaled_rect(self, display_size: tuple[int, int]) -> pygame.Rect:
        display_width, display_height = display_size
        scale = min(
            display_width / self.config.logical_width,
            display_height / self.config.logical_height,
        )
        width = max(1, int(self.config.logical_width * scale))
        height = max(1, int(self.config.logical_height * scale))
        return pygame.Rect((display_width - width) // 2, (display_height - height) // 2, width, height)
