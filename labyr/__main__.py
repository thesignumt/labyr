import argparse
from importlib.metadata import PackageNotFoundError, version


def get_version():
    try:
        return version("labyr")
    except PackageNotFoundError:
        return "unknown"


def run_labyr(level=None):
    from .__init__ import labyr

    labyr(level=level)


def main():
    parser = argparse.ArgumentParser(
        description="labyr: a labyrinth game || DISCLAIMER: if you run labyr, each frame will clear the terminal screen."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"labyr {get_version()}",
        help="Show labyr version",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        metavar="x",
        help="Set the labyrinth level (number)",
    )
    parser.add_argument(
        "action",
        choices=["run", "nil"],
        help="Action to perform. Allowed values: run, nil",
    )
    args = parser.parse_args()
    actions = {"run": lambda: run_labyr(level=args.level), "nil": lambda: None}
    actions[args.action]()


if __name__ == "__main__":
    main()
