from typing import Any, Dict, List, Union

import sys
import os
import json

# This is used to keep paths relative to where the program is unpacked in the temp dir
bundle_dir: str = getattr(
    sys,
    '_MEIPASS',
    os.path.abspath(os.path.dirname(__file__))
)


def get_path_in_bundle_dir(path: str) -> str:
    """
    Returns absolute path equivalent for given path
    """
    return os.path.abspath(os.path.join(bundle_dir, path))


def load_json(file_path: str) -> Union[Dict, Dict[str, List[str]]]:
    """
    Loads json file at given path and returns it as dict
    """

    file_path = get_path_in_bundle_dir(file_path)
    print(file_path)

    with open(file_path) as _file:
        return json.load(_file)
