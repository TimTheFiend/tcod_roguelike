from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov
from tcod import FOV_DIAMOND

from input_handlers import (
    EventHandler,
)

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap

class Engine:
    game_map: GameMap

    def __init__(
        self,
        player: Entity,
    ):
        self.event_handler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            continue
            print(f'{entity.name} thinks about where it all went wrong.')

    def update_fov(self):
        """Recompute the visible area based on the player's POV."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8,
            algorithm=FOV_DIAMOND
        )
        # If a tile is visible it should be added to `explored`
        self.game_map.explored |= self.game_map.visible  # Sets the explored array to include everything in the visible array


    def render(self, console: Console, context: Context):
        self.game_map.render(console)
        context.present(console)
        console.clear()
