# Pokedex

A small 160x128 Pokédex UI rendered with Pillow.

## Display Mode

Set display mode in `.env`:

```env
IS_RASPBERRY=0
```

- `IS_RASPBERRY=0`: render to a scaled desktop window for macOS development
- `IS_RASPBERRY=1`: render to the ST7735 TFT display

## Run

```bash
pip install -e .
pokedex
```

Keyboard controls in window mode:

- Arrow keys: move
- Enter or Z: select
- Escape or X: back
