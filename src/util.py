import json
from pathlib import Path


def load_json_file(path: str | Path):
    with open(path, "rb") as json_file:
        return json.load(json_file)
