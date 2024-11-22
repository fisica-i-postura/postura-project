import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


def read_json_to_dataclass(path: Path, cls: Any) -> Any:
    with open(path, 'r') as file:
        data = json.load(file)
    return cls(**data)


def write_dataclass_to_json(path: Path, obj: Any):
    with open(path, 'w') as file:
        json.dump(asdict(obj), file, indent=4)