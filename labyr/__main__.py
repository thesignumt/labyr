import argparse
from importlib.metadata import PackageNotFoundError, version


def get_version():
    try:
        return version("labyr")  # pypi project name
    except PackageNotFoundError:
        return "unknown"


def main():
    parser = argparse.ArgumentParser(description="labyr: a labyrinth game")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"labyr {get_version()}",
        help="Show labyr version",
    )

    args = parser.parse_args()


if __name__ == "__main__":
    main()
