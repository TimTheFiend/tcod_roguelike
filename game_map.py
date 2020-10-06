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

        # All tiles
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order='F')

        self.visible = np.full((width, height), fill_value=False, order='F')
        self.explored = np.full((width, height), fill_value=False, order='F')

    def in_bounds(self, x: int, y: int) -> bool:
        """Returns a bool based on if `x` and `y` is within bounds of the map."""
        return 0 <= x <= self.width and 0 <= y <= self.height

    def render(self, console: Console) -> None:
        """Using the `Console` class's `tiles_rgb` method, we can quickly render the entire map.

        If a tile is in the `self.visible` array, then draw it with the `light` colors.
        If it isn't, but it's in the explored array, draw it with 'dark' colors.
        Otherwise, draw it as `SHROUD`
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles['light'], self.tiles['dark']],
            default=tile_types.SHROUD
        )