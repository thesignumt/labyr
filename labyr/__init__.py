from typing import Any, Callable, Dict, List, Tuple

from utils.color import C

__all__ = ["labyr", "LabyrGame"]


def genlvls(
    chars: Dict[str, Tuple[str, Callable]],
    lvlSizes: Dict[int, Tuple[int, int]],
    *,
    c: C,
):
    out = {}
    SPACE_DEFAULT = (".", c.dark_gray)
    WALL_DEFAULT = ("#", c.dark_gray)
    PLAYER_DEFAULT = ("@", c.blue)
    EXIT_DEFAULT = ("E", c.green)
    MONSTER_DEFAULT = ("M", c.red)

    def init(dimen: Tuple[int, int]) -> List[List[str]]:
        space = chars.get("space", SPACE_DEFAULT)[0]
        x, y = dimen
        grid = [[space] * x for _ in range(y)]

        for i in range(x):
            for j in range(y):
                if i == 0 or i == x - 1 or j == 0 or j == y - 1:
                    grid[i][j] = "#"

        return grid

    for lvl, dimen in lvlSizes.items():
        out[lvl] = init(dimen)

    print(out)


class LabyrGame:
    def __init__(self) -> None:
        c = C()
        self.clvl = 0
        self.chars = {
            "space": (".", c.dark_gray),
            "wall": ("#", c.dark_gray),
            "player": ("@", c.blue),
            "exit": ("E", c.green),
            "monster": ("M", c.red),
        }
        lvlSizes = {0: (5, 3)}
        levels = genlvls(self.chars, lvlSizes, c=c)


labyr = LabyrGame()
