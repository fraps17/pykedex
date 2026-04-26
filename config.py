from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_env(path: Path = BASE_DIR / ".env") -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class Config:
    logical_width: int = 160
    logical_height: int = 128
    scale: int = 4
    fps: int = 30
    is_raspberry: bool = False
    data_path: Path = BASE_DIR / "data" / "pokemon.json"

    @classmethod
    def from_env(cls) -> "Config":
        env = load_env()
        return cls(is_raspberry=env.get("IS_RASPBERRY", "0") == "1")

    @property
    def logical_size(self) -> tuple[int, int]:
        return (self.logical_width, self.logical_height)

    def __post_init__(self) -> None:
        if self.scale < 1:
            raise ValueError("scale must be at least 1")
        if self.fps < 1:
            raise ValueError("fps must be at least 1")
