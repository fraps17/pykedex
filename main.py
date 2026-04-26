from __future__ import annotations

import pygame

try:
    from . import display
except ImportError:
    import display


def main() -> None:
    pygame.init()
    clock = pygame.time.Clock()
    surface = pygame.Surface((display.WIDTH, display.HEIGHT))

    try:
        while True:
            surface.fill((0, 180, 80))
            display.render(surface)
            clock.tick(30)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
