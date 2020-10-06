from typing import Set, Iterable, Any, TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console

from entity import (
    Entity,
)
from game_map import GameMap
from input_handlers import (
    EventHandler,
)

if TYPE_CHECKING:
    from entity import Entity

class Engine:
    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            # No valid action
            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context):
        self.game_map.render(console)

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)
        console.clear()