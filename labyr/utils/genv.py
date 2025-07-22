import os
from pathlib import Path


class GlobalEnv:
    def __init__(self):
        self._init_paths()
        self._load()

    def _init_paths(self):
        local_appdata = os.getenv("LOCALAPPDATA")
        if not local_appdata:
            raise EnvironmentError("LOCALAPPDATA environment variable not found.")
        self._dir = Path(local_appdata) / "test"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._filename = self._dir / ".envdata.db"

    def _load(self):
        try:
            with open(self._filename, "rb") as f:
                import pickle

                self._store = pickle.load(f)
        except Exception:
            self._store = {}

    def _save(self):
        with open(self._filename, "wb") as f:
            import pickle

            pickle.dump(self._store, f)

    def __getattr__(self, name):
        try:
            return self._store[name]
        except KeyError:
            raise AttributeError(f"'_G' has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._store[name] = value
            self._save()

    def __getitem__(self, key):
        return self._store[key]

    def __setitem__(self, key, value):
        self._store[key] = value
        self._save()

    def clear(self):
        self._store.clear()
        self._save()

    def reinit(self):
        self.clear()
        self._load()


_G = GlobalEnv()
