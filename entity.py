from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar('T', bound='Entity')


class Entity:
    """Generic object."""
    gamemap: GameMap

    def __init__(
            self,
            gamemap: Optional[GameMap] = None,
            x: int = 0,
            y: int = 0,
            char: str = '?',
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = '<Unnamed',
            blocks_movement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if gamemap:
            # If `gamemap` isn't provided now then it will be set later
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: GameMap, x: int, y: int):
        """Spawn a copy of this instance at a given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None):
        """Place the entity at a new location. Handles moving across `GameMap`s"""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"):  # Possibly uninitialized.
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dest_x: int, dest_y: int) -> None:
        self.x += dest_x
        self.y += dest_y
