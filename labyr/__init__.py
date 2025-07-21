from sys import exit as _exit
from time import sleep as tsleep
from typing import Any

from ._secret import Secret
from .utils import box, clsscr, color, getch, getchar
from .utils.dot import Dot
from .utils.entity import Actiwall, EntMan, Player, handlemove
from .utils.fill import fill_rect
from .utils.transform import get_map

__all__ = ["labyr", "LabyrGame"]


def genlvls(
    chars: dict,
    lvlSizes: dict[int, tuple[int, int]],
):
    out = {}

    def init(dimen: tuple[int, int]) -> list[list[str]]:
        """generate walls"""
        space = getchar(chars, "space")[0]
        x, y = dimen
        grid = [[space] * x for _ in range(y)]

        for i in range(x):
            for j in range(y):
                if i == 0 or i == x - 1 or j == 0 or j == y - 1:
                    grid[j][i] = "#"

        return grid

    for lvl, dimen in lvlSizes.items():
        out[lvl] = init(dimen)

    space_char = getchar(chars, "space")[0]
    wall_char = getchar(chars, "wall")[0]
    actiwall_char = getchar(chars, "actiwall")[0]
    player_char = getchar(chars, "player")[0]
    exit_char = getchar(chars, "exit")[0]

    def set_chars(out, lvl, positions, char, **kwds):
        actiwall = kwds.get("actiwall")
        if actiwall:
            value = (
                char,
                Actiwall(
                    actiwall["pos"],
                    actiwall["goto"],
                    actiwall["plate"],
                    actiwall["retplate"],
                ),
            )
        else:
            value = char

        # Normalize positions to a list of tuples
        if (
            isinstance(positions, tuple)
            and len(positions) == 2
            and all(isinstance(i, int) for i in positions)
        ):
            positions = [positions]

        for y, x in positions:
            out[lvl][y][x] = value

    def rect(y1: int, x1: int, y2: int, x2: int):
        return ((y1, x1), (y2, x2))

    def srect(y: int, x: int):
        return ((y, x), (y, x))

    level_defs = [
        # lvl 0 conf
        # #######
        # #@...E#
        # #######
        {"player": [(1, 1)], "exit": [(1, 5)], "walls": [], "spaces": []},
        # lvl 1 conf
        # ###########
        # #@......#E#
        # #######.#.#
        # #.......#.#
        # #.#######.#
        # #.........#
        # ###########
        {
            "player": [(1, 1)],
            "exit": [(1, -2)],
            "walls": [
                rect(2, 1, 2, 6),
                rect(4, 2, 4, -3),
                rect(1, -3, 3, -3),
            ],
            "spaces": [],
        },
        # lvl 2 conf
        # ...######...
        # ####....####
        # #@...##...E#
        # ####....####
        # ...######...
        {
            "player": [(2, 1)],
            "exit": [(2, -2)],
            "walls": [
                rect(1, 1, 1, 3),
                rect(1, -4, 1, -2),
                rect(3, 1, 3, 3),
                rect(3, -4, 3, -2),
                rect(2, 5, 2, 6),
            ],
            "spaces": [
                rect(0, 0, 0, 2),
                rect(-1, 0, -1, 2),
                rect(0, -3, 0, -1),
                rect(-1, -3, -1, -1),
            ],
        },
        # lvl 3 conf
        # ###########
        # #@...#..###
        # ###.#....E#
        # #.....#..##
        # ###########
        {
            "player": [(1, 1)],
            "exit": [(2, -2)],
            "walls": [
                rect(2, 1, 2, 2),
                rect(2, 4, 2, 4),
                rect(1, 5, 1, 5),
                rect(3, 6, 3, 6),
                rect(3, -2, 3, -2),
                rect(1, -3, 1, -2),
            ],
            "spaces": [],
        },
        # lvl 4 conf
        # ......###......
        # #######.#######
        # #@....&.&....E#
        # ####.##.##.####
        # ...#...&...#...
        # ...####.####...
        {
            "player": [(1, 1)],
            "exit": [(1, -2)],
            "actiwalls": [
                {
                    "pos": (1, 6),
                    "goto": (0, 7),
                    "plate": Dot({"pos": (1, 5), "dir": "d"}),
                    "retplate": Dot({"pos": (1, 9), "dir": "d"}),
                },
                {
                    "pos": (1, 8),
                    "goto": (2, 7),
                    "plate": Dot({"pos": (1, 5), "dir": "d"}),
                    "retplate": Dot({"pos": (1, 9), "dir": "d"}),
                },
            ],
            "spaces": [
                rect(0, 0, 0, -1),
                rect(1, 7, 3, 7),
                rect(3, 4, 4, 6),
                rect(3, 8, 4, 10),
            ],
            "walls": [
                rect(0, 6, 0, 8),
                rect(3, 5, 3, 6),
                rect(3, 8, 3, 9),
                rect(3, 1, 3, 3),
                rect(3, -1, 3, -3),
                rect(4, 0, 5, 2),
                rect(4, -3, 5, -1),
                srect(4, 3),
                srect(4, -4),
            ],
        },
    ]

    for lvl, conf in enumerate(level_defs):
        for k in ["walls", "spaces"]:
            conf.setdefault(k, [])
        set_chars(out, lvl, conf["player"], player_char)
        set_chars(out, lvl, conf["exit"], exit_char)
        if conf.get("actiwalls"):
            for actiwall_ in conf["actiwalls"]:
                set_chars(out, lvl, actiwall_["pos"], actiwall_char, actiwall=actiwall_)
                set_chars(out, lvl, actiwall_["goto"], space_char)
        for start, end in conf["walls"]:
            fill_rect(out[lvl], start, end, wall_char)
        for start, end in conf["spaces"]:
            fill_rect(out[lvl], start, end, space_char)

    return out


def cout_labyr(map: list[list[str]], chars: dict, clvl: int, entman: EntMan):
    chmap = get_map(chars)

    dir_map = {"w": "↑", "a": "←", "s": "↓", "d": "→"}
    revdir_map = {"w": "⇑", "a": "⇐", "s": "⇓", "d": "⇒"}
    actiwalls: list[Actiwall] = entman.get(clvl, "actiwalls")
    plate_pos: dict = {aw.plate.pos: dir_map.get(aw.plate.dir, "?") for aw in actiwalls}
    retplate_pos: dict = {
        aw.retplate.pos: revdir_map.get(aw.retplate.dir, "¿") for aw in actiwalls
    }

    DARKGRAY = color.C.dark_gray
    print("\n" + DARKGRAY(f"lvl: {clvl}"))
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            # Handle actiwall plate rendering
            px, py = entman.get(clvl, "player")
            if (y, x) != (py, px):
                if (y, x) in plate_pos:
                    print(DARKGRAY(plate_pos[(y, x)]), end="")
                    continue
                if (y, x) in retplate_pos:
                    print(DARKGRAY(retplate_pos[(y, x)]), end="")
                    continue

            ch = cell[0]

            if ch != "$" and ch in chmap:
                print(chmap[ch](ch), end="")
            elif isinstance(cell, str) and cell.startswith("$M"):
                print(chmap["M"]("M"), end="")
            elif isinstance(cell, tuple):
                print(chmap[ch](ch), end="")
            else:
                print(cell, end="")
        print()


class LabyrGame:
    def __init__(self, *, level=0) -> None:
        c = color.C()
        self.clvl = level
        self.chars = {
            "DEFAULTS": {
                "space": (".", c.dark_gray),
                "wall": ("#", c.dark_gray),
                "actiwall": ("&", c.light_gray),
                "player": ("@", c.blue),
                "exit": ("E", c.green),
                "monster": ("M", c.red),
            },
            "space": (".", c.dark_gray),
            "wall": ("#", c.dark_gray),
            "actiwall": ("&", c.light_gray),
            "player": ("@", c.blue),
            "exit": ("E", c.green),
            "monster": ("M", c.red),
        }
        self.__lvlSizes = {0: (7, 3), 1: (11, 7), 2: (12, 5), 3: (11, 5), 4: (15, 6)}
        self.levels = genlvls(self.chars, self.__lvlSizes)
        self.entman = EntMan(self.levels, self.chars)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        level = kwds.get("level")
        valid_levels = self.__lvlSizes.keys()
        if isinstance(level, int) and level in valid_levels:
            self.clvl = level
        else:
            if level is not None:
                print(
                    "\033[91mError: 'level must be an integer in {}.\033[0m".format(
                        list(valid_levels)
                    )
                )
                _exit(1)

        running: bool = True
        cmap = self.levels[self.clvl]

        refresh = lambda: (  # noqa: E731
            clsscr(),
            cout_labyr(cmap, self.chars, self.clvl, entman=self.entman),
        )

        win = False

        exit_char = getchar(self.chars, "exit")[0]
        while running:
            if win:
                clsscr()
                print(f"\n{box('YOU WONNNNN')}\n")
                tsleep(Secret())
                _exit(0)
            else:
                refresh()
            move = getch().lower()

            if move in ["w", "a", "s", "d"]:
                out = handlemove(self.chars, self.clvl, cmap, self.entman, move)
                if out == "ESCAPE":
                    refresh = lambda: (  # noqa: E731
                        clsscr(),
                        cout_labyr(cmap, self.chars, self.clvl, entman=self.entman),
                    )

                    nlvl = self.clvl + 1
                    if nlvl > max(self.__lvlSizes.keys()):
                        win = True
                        continue
                    else:
                        plyr = self.entman.get(self.clvl, "player")
                        x, y = plyr
                        refresh()
                        tsleep(0.3)
                        cmap[y][x] = exit_char
                        refresh()
                        tsleep(0.5)
                        self.clvl += 1
                        cmap = self.levels[self.clvl]
            elif move == "r":
                self.levels = genlvls(self.chars, self.__lvlSizes)
                self.entman = EntMan(self.levels, self.chars)
                cmap = self.levels[self.clvl]
                clsscr()
            elif move == "q":
                clsscr()
                _exit(0)


labyr = LabyrGame()
