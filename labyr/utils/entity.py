from typing import Any

from . import getchar


class EntMan:
    """entity manager"""

    def __init__(self, levels: dict) -> None:
        pass

    def __getattribute__(self, name: str, /) -> Any:
        if name.startswith("l"):
            lvl = name[-1]
            print(lvl)
        else:
            print("not lvl idx")


class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y


def handlemove(chars, curMap: list, entity: Player, move: str):
    if not isinstance(entity, Player):
        return

    x, y = entity.x, entity.y
    move_offsets = {"w": (0, 1), "a": (-1, 0), "s": (0, -1), "d": (1, 0)}
    dx, dy = move_offsets.get(move, (0, 0))
    nx, ny = x + dx, y + dy

    if 0 <= ny < len(curMap) and 0 <= nx < len(curMap[0]):
        target = curMap[ny][nx]
        player_char = getchar(chars, "player")[0]
        space_char = getchar(chars, "space")[0]
        if target in (space_char,):
            curMap[y][x] = space_char
            curMap[ny][nx] = player_char
            entity.x, entity.y = nx, ny
