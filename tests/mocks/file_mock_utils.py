import json
import os
from typing import Union

from src.utils import file_utils



def get_http_file_content(file_name: str) -> Union[dict, list]:
    return get_file_content(file_name, "http")


def get_file_content(file_name: str, directory: str) -> Union[dict, list]:
    file_path = os.path.join(file_utils.get_project_root(), "tests", "resources", directory, file_name)
    with open(file_path) as file:
        return json.load(file)
