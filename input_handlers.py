from typing import Optional

import tcod.event

from actions import (
    Action,
    EscapeAction,
    MovementAction,
)


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        print('Exited via `ev_quit()`')
        raise SystemExit(0)

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = MovementAction(destination_x=0, destination_y=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(destination_x=0, destination_y=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(destination_x=-1, destination_y=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(destination_x=1, destination_y=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()


        # No valid keypress
        return action