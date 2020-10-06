from typing import Tuple

class Entity:
    """Generic object."""
    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dest_x: int, dest_y: int) -> None:
        self.x = dest_x
        self.y = dest_y