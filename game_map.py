import numpy as np
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(
        self,
        width: int,
        height: int,
    ):
        self.width = width
        self.height = height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order='F')


    def in_bounds(self, x: int, y: int) -> bool:
        """Returns a bool based on if `x` and `y` is within bounds of the map."""
        return 0 <= x <= self.width and 0 <= y <= self.height

    def render(self, console: Console) -> None:
        """Using the `Console` class's `tiles_rgb` method, we can quickly render the entire map."""
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles['dark']