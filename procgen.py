from __future__ import annotations

import random as rng
from typing import Iterator, List, Tuple, TYPE_CHECKING
from game_map import GameMap
import tile_types

import tcod

if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
    ):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Returns the cneter of the room as `(x, y)` coordinates"""
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of the room.

        A `slice` object is used to indicate how to "cut" up a collection, so what we return is the exact coordinates
        of where this `RectangularRoom` is in the `GameMap`

        We `+ 1` to take the walls of the room into account
        """
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def tunnel_between(
        start: Tuple[int, int],
        end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end

    if rng.random() < 0.5:  # 50% chance
        # Move horizontally,then vertically
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    # Generate coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        *,
        map_width: int,
        map_height: int,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []

    for i in range(max_rooms):
        room_width = rng.randint(room_min_size, room_max_size)
        room_height = rng.randint(room_min_size, room_max_size)

        x = rng.randint(0, dungeon.width - room_width - 1)
        y = rng.randint(0, dungeon.height - room_height - 1)

        # `RectangularRoom` class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # First room generated
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)
    return dungeon
