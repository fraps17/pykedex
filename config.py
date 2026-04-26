from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Config:
    logical_width: int = 160
    logical_height: int = 128
    scale: int = 4
    fps: int = 30
    fullscreen: bool = False
    data_path: Path = BASE_DIR / "data" / "pokemon.json"

    @property
    def logical_size(self) -> tuple[int, int]:
        return (self.logical_width, self.logical_height)

    @property
    def window_size(self) -> tuple[int, int]:
        return (self.logical_width * self.scale, self.logical_height * self.scale)

    def __post_init__(self) -> None:
        if self.scale < 1:
            raise ValueError("scale must be at least 1")
        if self.fps < 1:
            raise ValueError("fps must be at least 1")
