import traceback

import tcod

import color
import exceptions
import random
import input_handlers
import setup_game

import consts

def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """if the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print('Game saved.')

def main():
    print('HELLO')
    tileset = tcod.tileset.load_tilesheet(
        'Aesomatica16x16.png',
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )
    tileset2 = tcod.tileset.load_tilesheet(
        r"C:\Users\joak\repos\jap-rogue\res\tileset\Jolly16x16.png",
        16,
        16,
        tcod.tileset.CHARMAP_CP437,
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        consts.SCREEN_WIDTH,
        consts.SCREEN_HEIGHT,
        tileset=tileset,
        title='You know the drill',
        vsync=True,
    ) as context:
        root_console = tcod.Console(consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT, order='F')
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        if random.random() < 0.5:
                            context.change_tileset(tileset2)
                        else:
                            context.change_tileset(tileset)
                        handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error,
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            save_game(handler, "savegame.sav")
            raise
        except BaseException:
            save_game(handler, "savegame.sav")
            raise


if __name__ == '__main__':
    main()
