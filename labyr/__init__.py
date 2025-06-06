from typing import Any, Callable, Dict, List, Tuple

from .utils import color

__all__ = ["labyr", "LabyrGame"]


def genlvls(
    chars: Dict,
    lvlSizes: Dict[int, Tuple[int, int]],
):
    out = {}
    SPACE_DEFAULT = chars["DEFAULTS"]["space"]
    PLAYER_DEFAULT = chars["DEFAULTS"]["player"]

    def init(dimen: Tuple[int, int]) -> List[List[str]]:
        space = chars.get("space", SPACE_DEFAULT)[0]
        x, y = dimen
        grid = [[space] * x for _ in range(y)]

        for i in range(x):
            for j in range(y):
                if i == 0 or i == x - 1 or j == 0 or j == y - 1:
                    grid[j][i] = "#"

        return grid

    for lvl, dimen in lvlSizes.items():
        out[lvl] = init(dimen)

    # lvl configs
    # out[lvl][y][x]

    # lvl 0 conf
    out[0][1][1] = chars.get("player", PLAYER_DEFAULT)[0]

    return out


def cout_labyr(map: List[List[str]], chars: Dict):
    chmap = dict(list(chars.values()))
    print("\n\n")
    for i in range(len(map)):
        for j in range(len(map[0])):
            ch = map[i][j][0]
            if ch != "$":
                if ch == "@":
                    print(ch, end="")
                elif ch == "E":
                    print(ch, end="")
                else:
                    print(ch, end="")
            elif map[i][j][:2] == "$M":  # e.g. str: "$M1" means monster #1
                print("M", end="")
        print()


class LabyrGame:
    def __init__(self) -> None:
        c = color.C()
        self.clvl = 0
        self.chars = {
            "DEFAULTS": {
                "space": (".", c.dark_gray),
                "wall": ("#", c.dark_gray),
                "player": ("@", c.blue),
                "exit": ("E", c.green),
                "monster": ("M", c.red),
            },
            "space": (".", c.dark_gray),
            "wall": ("#", c.dark_gray),
            "player": ("@", c.blue),
            "exit": ("E", c.green),
            "monster": ("M", c.red),
        }
        lvlSizes = {0: (5, 3)}
        self.levels = genlvls(self.chars, lvlSizes)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        cout_labyr(self.levels[self.clvl], self.chars)


labyr = LabyrGame()
