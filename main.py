import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import (
    EventHandler,
)
from procgen import generate_dungeon

from consts import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAP_WIDTH,
    MAP_HEIGHT,
    ROOM_MAX_SIZE,
    ROOM_MIN_SIZE,
    ROOM_MAX_ROOMS
)

def main():
    tileset = tcod.tileset.load_tilesheet(
        'Synergy16x16.png',
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    event_handler = EventHandler()

    player = Entity(x=int(SCREEN_WIDTH / 2), y=int(SCREEN_HEIGHT / 2), char='@', color=(255, 255, 255))
    npc = Entity(x=int(SCREEN_WIDTH / 2 - 5), y=int(SCREEN_HEIGHT / 2 - 5), char='☺', color=(255,255,0))
    entities = {npc, player}

    game_map = generate_dungeon(
        map_width=MAP_WIDTH,
        map_height=MAP_HEIGHT,
        max_rooms=ROOM_MAX_ROOMS,
        room_max_size=ROOM_MAX_SIZE,
        room_min_size=ROOM_MIN_SIZE,
        player=player,
    )

    engine = Engine(
        entities=entities,
        event_handler=event_handler,
        game_map=game_map,
        player=player,
    )


    with tcod.context.new_terminal(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        tileset=tileset,
        title='You know the drill',
        vsync=True,
    ) as context:
        root_console = tcod.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order='F')

        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)


if __name__ == '__main__':
    main()