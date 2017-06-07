import json
import os


_FILEPATH_PARAMS_NAMES = "../../res/parameters_names.json"


def _get_name_from_file(value):
    filepath = os.path.join(os.path.dirname(__file__),
                            _FILEPATH_PARAMS_NAMES)
    with open(filepath) as file:
        return json.load(file)[value]


def id() -> str:
    return _get_name_from_file("identificator")


def training_values() -> str:
    return _get_name_from_file("training_values")


def database() -> str:
    return _get_name_from_file("database")


if __name__ == '__main__':
    pass
