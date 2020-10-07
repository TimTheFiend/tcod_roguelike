import copy
import traceback

import tcod

import color
from engine import Engine
from entity import Entity
import entity_factory
from procgen import generate_dungeon

import consts

def main():
    tileset = tcod.tileset.load_tilesheet(
        'Synergy16x16.png',
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    player = copy.deepcopy(entity_factory.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        map_width=consts.MAP_WIDTH,
        map_height=consts.MAP_HEIGHT,
        max_rooms=consts.ROOM_MAX_ROOMS,
        room_max_size=consts.ROOM_MAX_SIZE,
        room_min_size=consts.ROOM_MIN_SIZE,
        max_monsters_per_room=consts.ROOM_MAX_MONSTERS_PER_ROOM,
        max_items_per_room=consts.ROOM_MAX_ITEMS_PER_ROOM,
        engine=engine,
    )
    engine.update_fov()

    engine.message_log.add_message(
        'You came to the wrong neighborhood, motherfucker',
        color.welcome_text,
    )

    with tcod.context.new_terminal(
        consts.SCREEN_WIDTH,
        consts.SCREEN_HEIGHT,
        tileset=tileset,
        title='You know the drill',
        vsync=True,
    ) as context:
        root_console = tcod.Console(consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT, order='F')

        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:
                traceback.print_exc()
                engine.message_log.add_message(traceback.format_exc(), color.error)

if __name__ == '__main__':
    main()