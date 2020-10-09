from __future__ import annotations

from typing import Tuple, TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from entity import Actor
    from game_map import GameMap


def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ', '.join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def render_names_at_mouse_location(
        console: Console, x: int, y: int, engine: Engine,
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map,
    )

    console.print(x=x, y=y, string=names_at_mouse_location)

def render_bar(
        console: Console,
        total_width: int,
        player: Actor,
        x: int = 0,
        y: int = 0,
) -> None:
    bar_width = int(float(player.fighter.hp) / player.fighter.max_hp * total_width)
    # return

    console.draw_rect(
        x=x + 1,
        y=y,
        width=total_width,
        height=1,
        ch=1,
        bg=color.bar_empty
    )
    if bar_width > 0:
        console.draw_rect(
            x=x + 1,
            y=y,
            width=bar_width,
            height=1,
            ch=1,
            bg=color.bar_filled
        )

    console.print(
        x=x + 1,
        y=y,
        string=f'HP: {player.fighter.hp}/{player.fighter.max_hp}'.replace('0', 'o'),
        fg=color.bar_text,
    )


def render_character_stats(console: Console, player: Actor):
    """Renders the player's character stats, and HP inside a frame to the left."""
    y = 1
    x = 80
    total_width = console.width - x - 2
    height = 8

    print_outs = [
        f'Level: {player.level.current_level}',
        f'xp: {player.level.current_xp}',
        f'xp req.: {player.level.xp_to_next_level}',
        f'Attack: {player.fighter.power}',
        f'Defense: {player.fighter.defense}',
    ]

    if player.name[-1].lower() == 's':
        player_name = player.name + '\''
    else:
        player_name = player.name + '\'s'


    console.draw_frame(
        x=x,
        y=y - 1,
        width=console.width - x,
        height=height,
        title=f'{player_name} stats',
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )

    render_bar(console=console, total_width=total_width, player=player, x=x, y=y)

    for i, output in enumerate(print_outs):
        console.print(
            x=x + 1,
            y=y + i + 1,
            string=output.replace('0', 'o')
        )

    console.draw_frame(
        x=x,
        y=y - 1 + height,
        width=console.width - x,
        height=4,
        title=f'Equipment',
        clear=True,
        fg=(255, 255, 255),
        bg=(0, 0, 0),
    )
    console.print(
        x=x + 1,
        y=y + height,
        string=f'Weapon: {player.equipment.equipped_weapon}'
    )
    console.print(
        x=x + 1,
        y=y + 1 + height,
        string=f'Armor: {player.equipment.equipped_armor}'
    )




def render_dungeon_level(
        console: Console, dungeon_level: int, location: Tuple[int, int]
) -> None:
    x, y = location
    console.print(x=x, y=y, string=f'Dungeon level: {dungeon_level}')