from typing import Any

__all__ = ["labyr", "LabyrGame"]


def genlvls(chars: dict[str, str], lvlSizes: dict[int, tuple[int, int]]):
    out = {}
    SPACE_DEFAULT = " "
    PLAYER_DEFAULT = "@"
    WALL_DEFAULT = "#"
    EXIT_DEFAULT = "E"

    def init(x: int, y: int) -> list[list[str]]:
        space = chars.get("space", SPACE_DEFAULT)
        grid = [[space] * y for _ in range(x)]

        for i in range(x):
            for j in range(y):
                if i == 0 or i == x - 1 or j == 0 or j == y - 1:
                    grid[i][j] = "#"

        return grid

    print(init(lvlSizes[0][0], lvlSizes[0][1]))


class LabyrGame:
    def __init__(self) -> None:
        self.clvl = 0
        self.chars = {
            "space": ".",
            "wall": "#",
            "player": "@",
            "exit": "E",
        }
        lvlSizes = {0: (3, 5)}
        levels = genlvls(self.chars, lvlSizes)


labyr = LabyrGame()
