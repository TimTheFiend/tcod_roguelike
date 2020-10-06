from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity):
        """Perform this action with the objects needed to determine its scope.
        `engine` is the scope being performed in.
        `entity` is the object performing the action.
        This method must be overriden by action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity):
        raise SystemExit(0)



class MovementAction(Action):
    def __init__(self, destination_x: int, destination_y: int):
        super().__init__()

        self.dx = destination_x
        self.dy = destination_y


    def perform(self, engine: Engine, entity: Entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return  # Destination is not in bounds
        if not engine.game_map.tiles['walkable'][dest_x, dest_y]:
            return  # Destination is not walkable

        entity.move(dest_x=dest_x, dest_y=dest_y)