# AGENT.md — Pokédex App

## Goal

Build a Pokédex-style application for a Raspberry Pi Zero with a 1.8" TFT screen.

The app should behave like a small dedicated operating system: when the device powers on, it should boot directly into the Pokédex UI and stay there.

For development, the app must also run on macOS.

## Tech Direction

Use **Python + pygame**.

## Runtime Model

The app is not a real OS.

It is a fullscreen application launched automatically at boot.

    Power on
    → Raspberry Pi OS boots
    → systemd starts Pokédex app
    → fullscreen Pokédex interface appears

## Input Model

The entire app must be controllable with exactly **6 physical buttons**:

    UP
    DOWN
    LEFT
    RIGHT
    A
    B

### Button Meaning

- UP: move selection up
- DOWN: move selection down
- LEFT: previous item / section
- RIGHT: next item / section
- A: confirm / select
- B: back / cancel

Keyboard mapping (dev only):

    Arrow keys → UP / DOWN / LEFT / RIGHT
    Enter or Z → A
    Escape or X → B

## App Structure

    pokedex/
    ├── main.py
    ├── config.py
    ├── input.py
    ├── app.py
    ├── screens/
    │   ├── boot.py
    │   ├── home.py
    │   ├── pokemon_list.py
    │   ├── pokemon_detail.py
    │   └── settings.py
    ├── data/
    │   └── pokemon.json
    ├── assets/
    │   ├── sprites/
    │   ├── icons/
    │   ├── fonts/
    │   └── sounds/
    └── README.md

## Core Architecture

Each screen exposes:

    handle_event(event)
    update(dt)
    draw(surface)

Main loop:

    read input
    update current screen
    draw current screen
    flip display

## Screens

### Boot Screen

    POKÉDEX SYSTEM
    BOOTING...

### Home Screen

    Pokémon
    Search
    Settings
    Shutdown

### Pokémon List

Scrollable list (UP/DOWN/A/B).

### Pokémon Detail

Shows:

- name
- number
- type
- sprite
- stats
- description

Use LEFT/RIGHT for sections.

## Display

Target resolution:

    160x128

Rules:

- large text
- high contrast
- few items per screen
- no dense layouts

## Data

Local JSON:

    {
      "id": 25,
      "name": "Pikachu",
      "types": ["Electric"],
      "height": 0.4,
      "weight": 6.0,
      "description": "..."
    }

## Development Mode

- runs on macOS
- windowed
- keyboard input
- scaled display

  logical: 160x128  
   window: 640x512  
   scale: 4x

## Raspberry Pi Mode

- fullscreen
- no cursor
- autostart via systemd
- GPIO buttons
- TFT display output

## Constraint

All interactions must work with:

    UP / DOWN / LEFT / RIGHT / A / B

## First Milestone

- pygame window
- boot screen
- home menu
- Pokémon list
- Pokémon detail
- keyboard controls
- small-screen layout simulation
