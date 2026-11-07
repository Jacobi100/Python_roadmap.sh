import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .errors import DataError


def data_file():
    override = os.environ.get("EXPENSE_TRACKER_FILE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".expense_tracker.json"


def load_expenses():
    path = data_file()
    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise DataError(f"could not read expense data from {path}: {error}") from error

    if not isinstance(data, list):
        raise DataError(f"expense data in {path} must be a JSON list")
    return data


def save_expenses(expenses):
    path = data_file()
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary_name = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            json.dump(expenses, temporary, indent=2)
            temporary.write("\n")
        os.replace(temporary_name, path)
    except OSError as error:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
        raise DataError(f"could not save expense data to {path}: {error}") from error
