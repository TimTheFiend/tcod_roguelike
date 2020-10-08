from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
from consts import *
from engine import Engine
import entity_factory
import input_handlers
from procgen import generate_dungeon


background_image = tcod.image.load('a50b225d588bd016cc6b43b948423093.png')[:, :, :3]
# background_image = tcod.image.load('menu_background.png')[:, :, :3]

def new_game() -> Engine:
    player = copy.deepcopy(entity_factory.player)
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=ROOM_MAX_ROOMS,
        room_min_size=ROOM_MIN_SIZE,
        room_max_size=ROOM_MAX_SIZE,
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        max_monsters_per_room=ROOM_MAX_MONSTERS_PER_ROOM,
        max_items_per_room=ROOM_MAX_ITEMS_PER_ROOM,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        'You came to the wrong neighborhood, motherfucker',
        color.welcome_text,
    )
    return engine


def load_game(filename: str) -> Engine:
    """Attempts to load an Engine instance from a file."""
    with open(filename, 'rb') as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return Engine

class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0,)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "ALL WOMEN ARE QUEENS",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height // 2 - 4,
            'IF SHE BREATHES, SHE\'S A THOT',
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ['[N]ew Game', '[C]ontinue last game', '[Q]uit',]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64)
            )

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit(0)
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game('savegame.sav'))
            except FileNotFoundError as exc:
                traceback.print_exc()
                return input_handlers.PopupMessage(self, f'Failed to load save:\n{exc}')
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())
        return None