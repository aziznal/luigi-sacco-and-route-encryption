from typing import Any

import sys
import os
import json


bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


def get_path_in_bundle_dir(path):
    return os.path.abspath(os.path.join(bundle_dir, path))


def load_json(file_path: str) -> None:

    file_path = get_path_in_bundle_dir(file_path)
    print(file_path)

    with open(file_path) as _file:
        return json.load(_file)


def save_as_json(file_path: str, data: Any) -> None:

    raise NotImplementedError()

    file_path = get_path_in_bundle_dir(file_path)

    with open(file_path, 'w') as output_file:
        json.dump(data, output_file, indent=4)


