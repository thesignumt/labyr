from collections.abc import Iterable as IterableABC
from typing import Any, Callable, Iterable, TypeVar, cast


def get_map(d: dict):
    merged = dict(d)
    if "CONST" in d and isinstance(d["CONST"], dict):
        merged.update(d["CONST"])
    return {v[0]: v[1] for k, v in merged.items() if k not in ["DEFAULTS", "CONST"]}


TKey = TypeVar("TKey", bound=IterableABC[str])


def normKs(
    d: dict[str | IterableABC[str], Any],
    kT: Callable[[IterableABC[str]], TKey] | None = None,
) -> dict[TKey, Any]:
    """Normalize dict keys so all keys are tuples, optionally transforming with kT container type.

    Args:
        d: Input dict with keys that may be str or iterable of str.
        kT: Optional callable to transform each key (tuple of strings) into any container.
             Using `list` is not allowed because lists are unhashable.

    Returns:
        Dict with keys converted to chosen container type.

    Raises:
        TypeError: If kT is the list constructor, because lists cannot be dict keys.
    """
    if kT is list:
        raise TypeError(
            "Lists are not allowed as dict keys because they are unhashable."
        )

    normalized: dict[TKey, Any] = {}
    for k, v in d.items():
        if isinstance(k, str):
            new_key: IterableABC[str] = (k,)
        elif isinstance(k, IterableABC) and not isinstance(k, tuple):
            new_key = tuple(k)
        else:
            new_key = k  # already tuple or container

        if kT is not None:
            new_key = kT(new_key)

        # Cast to TKey so Pyright understands this is the correct key type
        normalized[cast(TKey, new_key)] = v

    return normalized


def transform(args: Iterable, f: Callable) -> list:
    return list(map(f, args))
