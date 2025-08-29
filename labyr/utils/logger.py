import datetime
import inspect
import os
import random
from pathlib import Path
from typing import Optional


def append(path, text: str, encoding: str = "utf-8") -> None:
    """
    Append text to a file safely and efficiently.

    Parameters
    ----------
    path : Path
        The file path to append to.
    text : str
        The text to append.
    encoding : str, optional
        File encoding (default is 'utf-8').

    Returns
    -------
    None
    """
    with path.open("a", encoding=encoding) as f:
        f.write(text)


class logmgr:
    """A lightweight logging manager for creating and appending to log files.

    Manages log files in a specified directory, creating new files with
    a timestamp and hex suffix (YY-MM-DD-HH:MM-abcdef.log). Supports enabling/disabling
    logging, limiting the number of log files, and appending messages with a clean format.

    Usage
    =====
    ```python
    # Initialize the logger
    logger = logmgr(
        f_opts={"name": "mylogs", "verbose": True},  # logs go to ~/.mylogs/
        max_logs=10,
        enable=True
    )

    # Create a new log file
    log_file = logger.mk_log()
    print(f"Log file created: {log_file}")

    # Log a simple message
    logger("Application started")

    # Log multiple expressions for debug purposes
    x = 42
    y = [1, 2, 3]
    z = {"key": "value"}

    logger(x, y, z)  # Will log values along with their shortened types

    # Another log entry
    logger("Processing complete")

    # Logs are appended automatically to the most recent log file
    ```

    Args:
        f_opts (dict[str, str], optional): Dictionary with keys:
            - 'name' (str): Folder name for logs under home directory (e.g., ~/.name/).
            - 'path' (str): Full path to log directory, overrides 'name' if provided.
            - 'verbose' or 'v' (bool): If True, includes line number, file name, and type in log entries.
            Either 'name' or 'path' must be specified, or a ValueError is raised.
        max_logs (int, optional): Maximum number of log files to keep (default: 100).
            If exceeded, the oldest log file is deleted.
        enable (bool, optional): Enables logging operations if True (default: False).
        verbose (bool, optional): Alias for f_opts['verbose'] or f_opts['v'] (default: False).

    Raises:
        ValueError: If neither 'name' nor 'path' is provided in f_opts, or if the log
            directory path is invalid (not a directory).
    """

    def __init__(
        self,
        f_opts: Optional[dict] = None,
        max_logs: int = 100,
        enable: bool = False,
        verbose: bool = False,
    ) -> None:
        f_opts = f_opts or {}
        if not isinstance(f_opts, dict):
            raise ValueError("f_opts must be a dictionary")
        if "path" in f_opts and f_opts["path"]:
            self.folder_path: Path = Path(f_opts["path"])
        elif "name" in f_opts and f_opts["name"]:
            self.folder_path: Path = Path.home() / f".{f_opts['name']}"
        else:
            raise ValueError("f_opts must contain either 'name' or 'path'")
        self.max_logs: int = max_logs
        self.enable: bool = enable
        self.verbose: bool = f_opts.get("verbose", f_opts.get("v", verbose))
        self._chk_dir()

    def _chk_dir(self) -> None:
        if not self.folder_path.exists():
            self.folder_path.mkdir(parents=True, exist_ok=True)
        if not self.folder_path.is_dir():
            raise ValueError(f"Path {self.folder_path} is not a directory")

    def _shorten_type(self, arg: object) -> str:
        """Shorten complex type names for readability, e.g., list[list[...]] for nested lists."""

        def get_type_name(t, depth=0, max_depth=2):
            type_name = t.__name__
            if type_name in ("list", "tuple", "dict", "set") and depth < max_depth:
                try:
                    # Get the type of the first element if available
                    if isinstance(arg, (list, tuple, set)) and arg:
                        inner = list(arg)[0]
                        inner_type = get_type_name(type(inner), depth + 1, max_depth)
                        return f"{type_name}[{inner_type}]"
                    elif isinstance(arg, dict) and arg:
                        inner = list(arg.values())[0]
                        inner_type = get_type_name(type(inner), depth + 1, max_depth)
                        return f"{type_name}[{inner_type}]"
                    return f"{type_name}[...]"
                except (IndexError, AttributeError):
                    return f"{type_name}[...]"
            return type_name

        return get_type_name(type(arg))

    def gen_logname(self) -> Optional[str]:
        if not self.enable:
            return None
        now = datetime.datetime.now()
        date = now.strftime("%y-%m-%d-%H:%M")
        rand = f"{random.getrandbits(24):06x}"
        return f"{date}-{rand}.log"

    def mk_log(self) -> Optional[str]:
        if not self.enable:
            return None
        fname = self.gen_logname()
        if not fname:
            return None
        fpath = self.folder_path / fname

        logs = [f for f in self.folder_path.glob("*.log")]
        if len(logs) >= self.max_logs:
            oldest = min(logs, key=lambda f: f.stat().st_birthtime)
            oldest.unlink()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[LOG] {timestamp}: Log created"
        if self.verbose:
            frame = inspect.currentframe().f_back  # pyright: ignore[reportOptionalMemberAccess]
            filename = os.path.basename(frame.f_code.co_filename)  # pyright: ignore[reportOptionalMemberAccess]
            log_entry += f" (line {frame.f_lineno}, {filename})"  # pyright: ignore[reportOptionalMemberAccess]
        log_entry += "\n"
        fpath.write_text(log_entry)
        return str(fpath)

    def __call__(self, *args) -> None:
        if not self.enable:
            return
        logs = list(self.folder_path.glob("*.log"))
        if not logs:
            # No log files exist, create a new one
            fpath = self.mk_log()
            if not fpath:
                return
        else:
            # Find the most recent log file by creation time
            fpath = max(logs, key=lambda f: f.stat().st_birthtime)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        frame = inspect.currentframe().f_back  # pyright: ignore[reportOptionalMemberAccess]
        filename = os.path.basename(frame.f_code.co_filename)  # pyright: ignore[reportOptionalMemberAccess]
        lineno = frame.f_lineno  # pyright: ignore[reportOptionalMemberAccess]

        if not args:
            return  # No arguments, nothing to log

        # Handle single string argument as a regular log message
        if len(args) == 1 and isinstance(args[0], str):
            log_entry = f"[LOG] {timestamp}: {args[0]}"
            if self.verbose:
                log_entry += f" (line {lineno}, {filename})"
            log_entry += "\n"
            append(fpath, log_entry)
            return

        # Debug mode: log expressions and their values with shortened type
        code = frame.f_code  # pyright: ignore[reportOptionalMemberAccess]
        source = inspect.getsourcelines(code)[0]
        call_line = source[frame.f_lineno - code.co_firstlineno]  # pyright: ignore[reportOptionalMemberAccess]
        # Extract the part of the line after the function call
        arg_str = call_line[call_line.index("(") + 1 : call_line.rindex(")")].strip()
        arg_expressions = [arg.strip() for arg in arg_str.split(",")] if arg_str else []

        # Log each argument with its expression, shortened type, and evaluated value
        for idx, (arg, expr) in enumerate(zip(args, arg_expressions)):
            arg_type = self._shorten_type(arg)
            if idx < len(arg_expressions):
                # Use the expression from the source code if available
                log_entry = f"[DEBUG] {timestamp}: {expr} ({arg_type}) -> {arg!r}"
            else:
                # Fallback for unnamed arguments
                log_entry = f"[DEBUG] {timestamp}: arg{idx} ({arg_type}) -> {arg!r}"
            if self.verbose:
                log_entry += f" (line {lineno}, {filename})"
            log_entry += "\n"
            append(fpath, log_entry)
